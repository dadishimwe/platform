"""
Notification-related models for the Starlink Platform API.
"""
from datetime import datetime
from src.models import db
from src.models.base import BaseModel

class NotificationTemplate(BaseModel):
    """Notification Template model."""
    __tablename__ = 'notification_templates'
    
    name = db.Column(db.String(100), unique=True, nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    
    # Relationships
    notifications = db.relationship('Notification', back_populates='template')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'subject': self.subject,
            'content': self.content,
            'type': self.type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<NotificationTemplate {self.name}>'


class Notification(BaseModel):
    """Notification model."""
    __tablename__ = 'notifications'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    template_id = db.Column(db.String(36), db.ForeignKey('notification_templates.id'), nullable=False)
    data = db.Column(db.JSON)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', back_populates='notifications')
    template = db.relationship('NotificationTemplate', back_populates='notifications')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'template_id': self.template_id,
            'data': self.data,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Notification {self.id}:{self.user_id}>'


class AlertConfiguration(BaseModel):
    """Alert Configuration model."""
    __tablename__ = 'alert_configurations'
    
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'))
    alert_type = db.Column(db.String(50), nullable=False)
    threshold = db.Column(db.Float)
    comparison = db.Column(db.String(10), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='alert_configurations')
    device = db.relationship('Device', back_populates='alert_configurations')
    notifications = db.relationship('AlertNotification', back_populates='alert_config', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'device_id': self.device_id,
            'alert_type': self.alert_type,
            'threshold': self.threshold,
            'comparison': self.comparison,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AlertConfiguration {self.id}:{self.alert_type}>'


class AlertNotification(BaseModel):
    """Alert Notification model."""
    __tablename__ = 'alert_notifications'
    
    alert_config_id = db.Column(db.String(36), db.ForeignKey('alert_configurations.id', ondelete='CASCADE'), nullable=False)
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    value = db.Column(db.Float)
    triggered_at = db.Column(db.DateTime, nullable=False)
    resolved_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    alert_config = db.relationship('AlertConfiguration', back_populates='notifications')
    device = db.relationship('Device', back_populates='alert_notifications')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'alert_config_id': self.alert_config_id,
            'device_id': self.device_id,
            'value': self.value,
            'triggered_at': self.triggered_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<AlertNotification {self.id}:{self.alert_config_id}>'


class NotificationPreference(BaseModel):
    """Notification Preference model."""
    __tablename__ = 'notification_preferences'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    email_enabled = db.Column(db.Boolean, default=True)
    push_enabled = db.Column(db.Boolean, default=True)
    in_app_enabled = db.Column(db.Boolean, default=True)
    
    # Relationships
    user = db.relationship('User', back_populates='notification_preferences')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'notification_type', name='uq_user_notification_type'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'notification_type': self.notification_type,
            'email_enabled': self.email_enabled,
            'push_enabled': self.push_enabled,
            'in_app_enabled': self.in_app_enabled,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<NotificationPreference {self.user_id}:{self.notification_type}>'

