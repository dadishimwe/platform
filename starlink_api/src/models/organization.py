"""
Organization-related models for the Starlink Platform API.
"""
from datetime import datetime
from src.models import db
from src.models.base import BaseModel

class Organization(BaseModel):
    """Organization model."""
    __tablename__ = 'organizations'
    
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    parent_id = db.Column(db.String(36), db.ForeignKey('organizations.id'))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    parent = db.relationship('Organization', remote_side=[id], backref=db.backref('children', lazy='dynamic'))
    users = db.relationship('OrganizationUser', back_populates='organization')
    service_plans = db.relationship('OrganizationServicePlan', back_populates='organization')
    devices = db.relationship('Device', back_populates='organization')
    tickets = db.relationship('Ticket', back_populates='organization')
    user_roles = db.relationship('UserRole', back_populates='organization')
    alert_configurations = db.relationship('AlertConfiguration', back_populates='organization')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'logo_url': self.logo_url,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Organization {self.name}>'


class OrganizationUser(db.Model):
    """Organization-User association model."""
    __tablename__ = 'organization_users'
    
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_primary = db.Column(db.Boolean, default=False)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='users')
    user = db.relationship('User', back_populates='organization_users')
    
    def __repr__(self):
        return f'<OrganizationUser {self.organization_id}:{self.user_id}>'


class ServicePlan(BaseModel):
    """Service Plan model."""
    __tablename__ = 'service_plans'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    data_limit_gb = db.Column(db.Numeric)
    speed_limit_mbps = db.Column(db.Numeric)
    price = db.Column(db.Numeric)
    currency = db.Column(db.String(3), default='USD')
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    organizations = db.relationship('OrganizationServicePlan', back_populates='service_plan')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'data_limit_gb': float(self.data_limit_gb) if self.data_limit_gb else None,
            'speed_limit_mbps': float(self.speed_limit_mbps) if self.speed_limit_mbps else None,
            'price': float(self.price) if self.price else None,
            'currency': self.currency,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ServicePlan {self.name}>'


class OrganizationServicePlan(db.Model):
    """Organization-ServicePlan association model."""
    __tablename__ = 'organization_service_plans'
    
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), primary_key=True)
    service_plan_id = db.Column(db.String(36), db.ForeignKey('service_plans.id', ondelete='CASCADE'), primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='service_plans')
    service_plan = db.relationship('ServicePlan', back_populates='organizations')
    
    def __repr__(self):
        return f'<OrganizationServicePlan {self.organization_id}:{self.service_plan_id}>'

