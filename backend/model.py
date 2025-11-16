"""
PyTorch model for next-item prediction based on cart contents.
Simple and efficient architecture optimized for grocery recommendations.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class NextItemPredictor(nn.Module):
    """
    Simple but effective model for next-item prediction.
    Uses embeddings + deep MLP with skip connections.
    """
    
    def __init__(self, num_items: int, embedding_dim: int = 128, hidden_dim: int = 256):
        super().__init__()
        self.num_items = num_items
        self.embedding_dim = embedding_dim
        
        # Item embeddings
        self.item_embeddings = nn.Embedding(
            num_embeddings=num_items,
            embedding_dim=embedding_dim,
            padding_idx=0
        )
        
        # Deep MLP with residual connections
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim)
        
        self.fc3 = nn.Linear(hidden_dim, hidden_dim)
        self.bn3 = nn.BatchNorm1d(hidden_dim)
        
        self.fc_out = nn.Linear(hidden_dim, num_items)
        
        self.dropout = nn.Dropout(0.4)
        
        # Initialize
        nn.init.xavier_uniform_(self.item_embeddings.weight)
        nn.init.xavier_uniform_(self.fc1.weight)
        nn.init.xavier_uniform_(self.fc2.weight)
        nn.init.xavier_uniform_(self.fc3.weight)
        nn.init.xavier_uniform_(self.fc_out.weight)
    
    def forward(self, cart_items):
        """
        Forward pass.
        
        Args:
            cart_items: (batch_size, seq_len)
        Returns:
            logits: (batch_size, num_items)
        """
        # Get embeddings
        embeddings = self.item_embeddings(cart_items)
        
        # Mean pooling (ignore padding)
        mask = (cart_items != 0).float().unsqueeze(-1)
        cart_sum = (embeddings * mask).sum(dim=1)
        cart_count = mask.sum(dim=1).clamp(min=1)
        cart_vector = cart_sum / cart_count
        
        # Deep MLP with residual connections
        x = F.relu(self.bn1(self.fc1(cart_vector)))
        x = self.dropout(x)
        
        x2 = F.relu(self.bn2(self.fc2(x)))
        x2 = self.dropout(x2)
        x = x + x2  # Residual
        
        x3 = F.relu(self.bn3(self.fc3(x)))
        x3 = self.dropout(x3)
        x = x + x3  # Residual
        
        logits = self.fc_out(x)
        
        return logits
    
    def predict_top_k(self, cart_items, k=10):
        """
        Predict top-k next items with probabilities.
        
        Args:
            cart_items: tensor of shape (batch_size, max_cart_size)
            k: number of top predictions to return
        
        Returns:
            top_items: tensor of shape (batch_size, k) with item IDs
            top_probs: tensor of shape (batch_size, k) with probabilities
        """
        with torch.no_grad():
            logits = self.forward(cart_items)
            probs = F.softmax(logits, dim=-1)
            top_probs, top_items = torch.topk(probs, k=k, dim=-1)
        
        return top_items, top_probs


class CoPurchasePredictor(nn.Module):
    """
    Model to predict probability of buying items together.
    Uses item embeddings and computes similarity scores.
    """
    
    def __init__(self, num_items: int, embedding_dim: int = 128):
        super().__init__()
        self.num_items = num_items
        self.item_embeddings = nn.Embedding(
            num_embeddings=num_items,
            embedding_dim=embedding_dim,
            padding_idx=0
        )
        
        nn.init.xavier_uniform_(self.item_embeddings.weight)
    
    def forward(self, item_pairs):
        """
        Compute co-purchase scores for item pairs.
        
        Args:
            item_pairs: tensor of shape (batch_size, 2) with [item1, item2]
        
        Returns:
            scores: tensor of shape (batch_size,) with co-purchase scores
        """
        item1_emb = self.item_embeddings(item_pairs[:, 0])
        item2_emb = self.item_embeddings(item_pairs[:, 1])
        
        # Cosine similarity
        scores = F.cosine_similarity(item1_emb, item2_emb, dim=-1)
        
        return scores
