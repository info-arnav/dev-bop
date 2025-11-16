"""
Train next-item prediction model on Instacart dataset.
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from model import NextItemPredictor
from preprocess_instacart import InstacartPreprocessor
import time
import os

class CartDataset(Dataset):
    """PyTorch dataset for cart sequences."""
    
    def __init__(self, carts, next_items):
        self.carts = carts
        self.next_items = next_items
    
    def __len__(self):
        return len(self.carts)
    
    def __getitem__(self, idx):
        return self.carts[idx], self.next_items[idx]

def collate_fn(batch):
    """Collate function to handle variable-length sequences."""
    carts, next_items = zip(*batch)
    
    # Pad sequences
    max_len = max(len(cart) for cart in carts)
    padded_carts = []
    for cart in carts:
        padded = cart + [0] * (max_len - len(cart))
        padded_carts.append(padded)
    
    return (
        torch.LongTensor(padded_carts),
        torch.LongTensor(next_items)
    )

def train_epoch(model, dataloader, optimizer, criterion, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    num_batches = 0
    
    for batch_idx, (carts, next_items) in enumerate(dataloader):
        carts = carts.to(device)
        next_items = next_items.to(device)
        
        optimizer.zero_grad()
        outputs = model(carts)
        loss = criterion(outputs, next_items)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        num_batches += 1
        
        if (batch_idx + 1) % 100 == 0:
            print(f"  Batch {batch_idx + 1}/{len(dataloader)}, Loss: {loss.item():.4f}")
    
    return total_loss / num_batches

def evaluate(model, dataloader, criterion, device, k_values=[1, 5, 10]):
    """Evaluate the model."""
    model.eval()
    total_loss = 0
    num_batches = 0
    
    # For top-k accuracy
    correct_at_k = {k: 0 for k in k_values}
    total = 0
    
    with torch.no_grad():
        for carts, next_items in dataloader:
            carts = carts.to(device)
            next_items = next_items.to(device)
            
            outputs = model(carts)
            loss = criterion(outputs, next_items)
            total_loss += loss.item()
            num_batches += 1
            
            # Calculate top-k accuracy
            for k in k_values:
                _, top_k_preds = outputs.topk(k, dim=1)
                correct_at_k[k] += (top_k_preds == next_items.unsqueeze(1)).any(dim=1).sum().item()
            
            total += next_items.size(0)
    
    avg_loss = total_loss / num_batches
    accuracy_at_k = {k: correct_at_k[k] / total for k in k_values}
    
    return avg_loss, accuracy_at_k

def main():
    # Configuration
    data_dir = '../data'
    vocab_path = './models/vocabulary.pkl'
    model_save_path = './models/best_model.pt'
    
    # Hyperparameters - optimized for speed and accuracy
    embedding_dim = 512
    hidden_dim = 1024
    batch_size = 4096    # Even larger batches for speed
    learning_rate = 0.001
    num_epochs = 8  # Fewer epochs, faster training
    sample_frac = 1.0
    min_product_count = 5000
    
    # Use MPS (Metal Performance Shaders) for M-series Macs
    if torch.backends.mps.is_available():
        device = torch.device('mps')
    elif torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    print(f"Using device: {device}")
    
    # Load or create preprocessor
    preprocessor = InstacartPreprocessor()
    
    if os.path.exists(vocab_path):
        print(f"Loading vocabulary from {vocab_path}...")
        preprocessor.load_vocabulary(vocab_path)
    else:
        print("Vocabulary not found. Please run generate_vocab_instacart.py first.")
        return
    
    # Process events
    print("\n" + "="*60)
    print("Processing Instacart Orders")
    print("="*60)
    carts, next_items, user_ids = preprocessor.process_events(
        data_dir,
        sample_frac=sample_frac,
        min_product_count=min_product_count
    )
    
    # Split into train/val
    split_idx = int(0.8 * len(carts))
    train_carts = carts[:split_idx]
    train_next_items = next_items[:split_idx]
    val_carts = carts[split_idx:]
    val_next_items = next_items[split_idx:]
    
    print(f"\nTrain examples: {len(train_carts):,}")
    print(f"Val examples: {len(val_carts):,}")
    
    # Create datasets
    train_dataset = CartDataset(train_carts, train_next_items)
    val_dataset = CartDataset(val_carts, val_next_items)
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=2
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=collate_fn,
        num_workers=2
    )
    
    # Create model
    print("\n" + "="*60)
    print("Initializing Model")
    print("="*60)
    model = NextItemPredictor(
        num_items=preprocessor.num_items,
        embedding_dim=embedding_dim,
        hidden_dim=hidden_dim
    ).to(device)
    
    num_params = sum(p.numel() for p in model.parameters())
    print(f"Model has {num_params:,} parameters")
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    print("\n" + "="*60)
    print("Training")
    print("="*60)
    
    best_val_loss = float('inf')
    best_val_accuracy = {}
    
    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch + 1}/{num_epochs}")
        print("-" * 60)
        
        start_time = time.time()
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        epoch_time = time.time() - start_time
        
        print(f"Train loss: {train_loss:.4f}, Time: {epoch_time:.2f}s")
        
        # Validation
        val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)
        print(f"Val loss: {val_loss:.4f}")
        print(f"Val accuracy - Top-1: {val_accuracy[1]*100:.2f}%, Top-5: {val_accuracy[5]*100:.2f}%, Top-10: {val_accuracy[10]*100:.2f}%")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_val_accuracy = val_accuracy
            checkpoint = {
                'model_state_dict': model.state_dict(),
                'val_loss': val_loss,
                'val_accuracy': val_accuracy,
                'num_items': preprocessor.num_items,
                'embedding_dim': embedding_dim,
                'hidden_dim': hidden_dim,
                'epoch': epoch + 1
            }
            torch.save(checkpoint, model_save_path)
            print(f"✓ Saved best model (val_loss: {val_loss:.4f})")
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Best accuracy - Top-1: {best_val_accuracy[1]*100:.2f}%, Top-5: {best_val_accuracy[5]*100:.2f}%, Top-10: {best_val_accuracy[10]*100:.2f}%")
    print(f"Model saved to: {model_save_path}")

if __name__ == '__main__':
    main()
