"""
User-related models for the Starlink Platform API.
"""
import bcrypt
from src.models import db
from src.models.base import BaseModel

class User(BaseModel):
    """User model."""
    __tablename__ = 'users'
    
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255))
    reset_token = db.Column(db.String(255))
    reset_token_expires_at = db.Column(db.DateTime)
    
    # Relationships
    roles = db.relationship('UserRole', back_populates='user')
    organization_users = db.relationship('OrganizationUser', back_populates='user')
    tickets = db.relationship('Ticket', foreign_keys='Ticket.user_id', back_populates='user')
    assigned_tickets = db.relationship('Ticket', foreign_keys='Ticket.assigned_to', back_populates='assigned_user')
    ticket_comments = db.relationship('TicketComment', back_populates='user')
    kb_articles = db.relationship('KbArticle', back_populates='author')
    chat_sessions = db.relationship('ChatSession', foreign_keys='ChatSession.user_id', back_populates='user')
    agent_sessions = db.relationship('ChatSession', foreign_keys='ChatSession.agent_id', back_populates='agent')
    chat_messages = db.relationship('ChatMessage', back_populates='sender')
    notifications = db.relationship('Notification', back_populates='user')
    notification_preferences = db.relationship('NotificationPreference', back_populates='user')
    
    def __init__(self, email, password, first_name=None, last_name=None, phone=None):
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class Role(BaseModel):
    """Role model."""
    __tablename__ = 'roles'
    
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    permissions = db.relationship('RolePermission', back_populates='role')
    users = db.relationship('UserRole', back_populates='role')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(BaseModel):
    """Permission model."""
    __tablename__ = 'permissions'
    
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    resource = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    
    # Relationships
    roles = db.relationship('RolePermission', back_populates='permission')
    
    __table_args__ = (
        db.UniqueConstraint('resource', 'action', name='uq_resource_action'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'resource': self.resource,
            'action': self.action,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Permission {self.name}>'


class RolePermission(db.Model):
    """Role-Permission association model."""
    __tablename__ = 'role_permissions'
    
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.String(36), db.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    role = db.relationship('Role', back_populates='permissions')
    permission = db.relationship('Permission', back_populates='roles')
    
    def __repr__(self):
        return f'<RolePermission {self.role_id}:{self.permission_id}>'


class UserRole(db.Model):
    """User-Role association model."""
    __tablename__ = 'user_roles'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='roles')
    role = db.relationship('Role', back_populates='users')
    organization = db.relationship('Organization', back_populates='user_roles')
    
    def __repr__(self):
        return f'<UserRole {self.user_id}:{self.role_id}:{self.organization_id}>'

