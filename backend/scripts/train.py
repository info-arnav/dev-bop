"""
Training script for next-item prediction model.
Loads data, trains PyTorch model, and saves model checkpoint.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.model_selection import train_test_split
import os
import argparse
from tqdm import tqdm

from model import NextItemPredictor
from preprocess import DataPreprocessor, compute_item_popularity


class CartDataset(Dataset):
    """PyTorch Dataset for cart->next_item prediction."""
    
    def __init__(self, carts: np.ndarray, next_items: np.ndarray):
        self.carts = torch.from_numpy(carts).long()
        self.next_items = torch.from_numpy(next_items).long()
    
    def __len__(self):
        return len(self.carts)
    
    def __getitem__(self, idx):
        return self.carts[idx], self.next_items[idx]


def train_epoch(model, dataloader, optimizer, criterion, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for carts, next_items in tqdm(dataloader, desc="Training"):
        carts = carts.to(device)
        next_items = next_items.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        logits = model(carts)
        loss = criterion(logits, next_items)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Stats
        total_loss += loss.item()
        _, predicted = torch.max(logits, 1)
        total += next_items.size(0)
        correct += (predicted == next_items).sum().item()
    
    avg_loss = total_loss / len(dataloader)
    accuracy = 100 * correct / total
    return avg_loss, accuracy


def evaluate(model, dataloader, criterion, device, k_values=[1, 5, 10]):
    """Evaluate model on validation set."""
    model.eval()
    total_loss = 0
    top_k_correct = {k: 0 for k in k_values}
    total = 0
    
    with torch.no_grad():
        for carts, next_items in tqdm(dataloader, desc="Evaluating"):
            carts = carts.to(device)
            next_items = next_items.to(device)
            
            logits = model(carts)
            loss = criterion(logits, next_items)
            total_loss += loss.item()
            
            # Top-k accuracy
            for k in k_values:
                _, top_k = torch.topk(logits, k=k, dim=-1)
                top_k_correct[k] += (top_k == next_items.unsqueeze(1)).any(dim=1).sum().item()
            
            total += next_items.size(0)
    
    avg_loss = total_loss / len(dataloader)
    top_k_acc = {k: 100 * correct / total for k, correct in top_k_correct.items()}
    
    return avg_loss, top_k_acc


def main():
    parser = argparse.ArgumentParser(description="Train next-item prediction model")
    parser.add_argument("--data", type=str, default="../data/events.csv", help="Path to events CSV")
    parser.add_argument("--output-dir", type=str, default="./models", help="Directory to save models")
    parser.add_argument("--embedding-dim", type=int, default=128, help="Embedding dimension")
    parser.add_argument("--hidden-dim", type=int, default=256, help="Hidden layer dimension")
    parser.add_argument("--batch-size", type=int, default=256, help="Batch size")
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--max-cart-size", type=int, default=20, help="Maximum cart size")
    parser.add_argument("--sample-frac", type=float, default=1.0, help="Fraction of data to use (for testing)")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Preprocess data
    print("\n=== Data Preprocessing ===")
    preprocessor = DataPreprocessor()
    carts, next_items, visitor_ids = preprocessor.process_events(
        args.data,
        min_cart_size=1,
        max_cart_size=args.max_cart_size
    )
    
    # Sample data if requested (for quick testing)
    if args.sample_frac < 1.0:
        n_samples = int(len(carts) * args.sample_frac)
        indices = np.random.choice(len(carts), n_samples, replace=False)
        carts = [carts[i] for i in indices]
        next_items = [next_items[i] for i in indices]
        print(f"Sampled {len(carts)} examples ({args.sample_frac * 100}%)")
    
    # Pad carts
    carts_padded = preprocessor.pad_carts(carts, max_length=args.max_cart_size)
    next_items_array = np.array(next_items)
    
    # Split into train/val
    print("\n=== Splitting Data ===")
    train_carts, val_carts, train_next, val_next = train_test_split(
        carts_padded, next_items_array, test_size=0.2, random_state=42
    )
    print(f"Train size: {len(train_carts)}")
    print(f"Val size: {len(val_carts)}")
    
    # Create datasets
    train_dataset = CartDataset(train_carts, train_next)
    val_dataset = CartDataset(val_carts, val_next)
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=4)
    
    # Create model
    print("\n=== Model Architecture ===")
    model = NextItemPredictor(
        num_items=preprocessor.num_items,
        embedding_dim=args.embedding_dim,
        hidden_dim=args.hidden_dim
    )
    model = model.to(device)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=2, factor=0.5)
    
    # Training loop
    print("\n=== Training ===")
    best_val_loss = float('inf')
    
    for epoch in range(args.epochs):
        print(f"\nEpoch {epoch + 1}/{args.epochs}")
        
        # Train
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
        print(f"Train Loss: {train_loss:.4f}, Train Acc@1: {train_acc:.2f}%")
        
        # Validate
        val_loss, val_top_k = evaluate(model, val_loader, criterion, device)
        print(f"Val Loss: {val_loss:.4f}")
        for k, acc in val_top_k.items():
            print(f"Val Acc@{k}: {acc:.2f}%")
        
        # Learning rate scheduling
        scheduler.step(val_loss)
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
                'val_top_k': val_top_k,
                'num_items': preprocessor.num_items,
                'embedding_dim': args.embedding_dim,
                'hidden_dim': args.hidden_dim,
                'max_cart_size': args.max_cart_size
            }
            torch.save(checkpoint, os.path.join(args.output_dir, "best_model.pt"))
            print(f"✓ Saved best model (val_loss: {val_loss:.4f})")
    
    # Save vocabulary
    preprocessor.save_vocabulary(os.path.join(args.output_dir, "vocabulary.pkl"))
    
    # Save final model
    torch.save(checkpoint, os.path.join(args.output_dir, "final_model.pt"))
    
    print("\n=== Training Complete ===")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Models saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
