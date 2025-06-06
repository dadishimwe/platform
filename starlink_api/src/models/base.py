"""
Base model for all database models.
"""
import uuid
from datetime import datetime
from src.models import db

class BaseModel(db.Model):
    """Base model for all database models."""
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

