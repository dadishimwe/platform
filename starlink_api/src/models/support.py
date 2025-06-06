"""
Support-related models for the Starlink Platform API.
"""
from datetime import datetime
from src.models import db
from src.models.base import BaseModel

class Ticket(BaseModel):
    """Ticket model."""
    __tablename__ = 'tickets'
    
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='open')
    priority = db.Column(db.String(20), nullable=False, default='medium')
    assigned_to = db.Column(db.String(36), db.ForeignKey('users.id'))
    closed_at = db.Column(db.DateTime)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='tickets')
    user = db.relationship('User', foreign_keys=[user_id], back_populates='tickets')
    assigned_user = db.relationship('User', foreign_keys=[assigned_to], back_populates='assigned_tickets')
    comments = db.relationship('TicketComment', back_populates='ticket', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'user_id': self.user_id,
            'subject': self.subject,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Ticket {self.id}:{self.subject}>'


class TicketComment(BaseModel):
    """Ticket Comment model."""
    __tablename__ = 'ticket_comments'
    
    ticket_id = db.Column(db.String(36), db.ForeignKey('tickets.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    
    # Relationships
    ticket = db.relationship('Ticket', back_populates='comments')
    user = db.relationship('User', back_populates='ticket_comments')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<TicketComment {self.id}:{self.ticket_id}>'


class KbCategory(BaseModel):
    """Knowledge Base Category model."""
    __tablename__ = 'kb_categories'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.String(36), db.ForeignKey('kb_categories.id'))
    
    # Relationships
    parent = db.relationship('KbCategory', remote_side=[id], backref=db.backref('children', lazy='dynamic'))
    articles = db.relationship('KbArticle', back_populates='category', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<KbCategory {self.name}>'


class KbArticle(BaseModel):
    """Knowledge Base Article model."""
    __tablename__ = 'kb_articles'
    
    category_id = db.Column(db.String(36), db.ForeignKey('kb_categories.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    published_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    
    # Relationships
    category = db.relationship('KbCategory', back_populates='articles')
    author = db.relationship('User', back_populates='kb_articles')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'category_id': self.category_id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<KbArticle {self.title}>'


class ChatSession(BaseModel):
    """Chat Session model."""
    __tablename__ = 'chat_sessions'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    agent_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    status = db.Column(db.String(50), nullable=False, default='open')
    ended_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='chat_sessions')
    agent = db.relationship('User', foreign_keys=[agent_id], back_populates='agent_sessions')
    messages = db.relationship('ChatMessage', back_populates='session', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'agent_id': self.agent_id,
            'status': self.status,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ChatSession {self.id}:{self.user_id}>'


class ChatMessage(BaseModel):
    """Chat Message model."""
    __tablename__ = 'chat_messages'
    
    session_id = db.Column(db.String(36), db.ForeignKey('chat_sessions.id', ondelete='CASCADE'), nullable=False)
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Relationships
    session = db.relationship('ChatSession', back_populates='messages')
    sender = db.relationship('User', back_populates='chat_messages')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'sender_id': self.sender_id,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ChatMessage {self.id}:{self.session_id}>'

