"""
Device-related models for the Starlink Platform API.
"""
from datetime import datetime
from src.models import db
from src.models.base import BaseModel

class Device(BaseModel):
    """Device model."""
    __tablename__ = 'devices'
    
    device_id = db.Column(db.String(100), unique=True, nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    location = db.Column(db.String(255))  # Using String instead of GEOGRAPHY for simplicity
    h3_cell_id = db.Column(db.String(20))
    software_version = db.Column(db.String(50))
    hardware_version = db.Column(db.String(50))
    last_seen = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='devices')
    configurations = db.relationship('DeviceConfiguration', back_populates='device', cascade='all, delete-orphan')
    status = db.relationship('DeviceStatus', back_populates='device', cascade='all, delete-orphan')
    ip_allocations = db.relationship('IpAllocation', back_populates='device', cascade='all, delete-orphan')
    user_terminal_telemetry = db.relationship('UserTerminalTelemetry', back_populates='device')
    router_telemetry = db.relationship('RouterTelemetry', back_populates='device')
    alerts = db.relationship('Alert', back_populates='device')
    alert_configurations = db.relationship('AlertConfiguration', back_populates='device')
    alert_notifications = db.relationship('AlertNotification', back_populates='device')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_type': self.device_type,
            'organization_id': self.organization_id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'h3_cell_id': self.h3_cell_id,
            'software_version': self.software_version,
            'hardware_version': self.hardware_version,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Device {self.device_id}>'


class DeviceConfiguration(BaseModel):
    """Device Configuration model."""
    __tablename__ = 'device_configurations'
    
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    config_key = db.Column(db.String(100), nullable=False)
    config_value = db.Column(db.JSON, nullable=False)
    
    # Relationships
    device = db.relationship('Device', back_populates='configurations')
    
    __table_args__ = (
        db.UniqueConstraint('device_id', 'config_key', name='uq_device_config_key'),
    )
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<DeviceConfiguration {self.device_id}:{self.config_key}>'


class DeviceStatus(BaseModel):
    """Device Status model."""
    __tablename__ = 'device_status'
    
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    details = db.Column(db.JSON)
    
    # Relationships
    device = db.relationship('Device', back_populates='status')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'status': self.status,
            'details': self.details,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<DeviceStatus {self.device_id}:{self.status}>'


class IpAllocation(BaseModel):
    """IP Allocation model."""
    __tablename__ = 'ip_allocations'
    
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    ipv4 = db.Column(db.String(15))
    ipv6_ue = db.Column(db.String(45))
    ipv6_cpe = db.Column(db.String(45))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    device = db.relationship('Device', back_populates='ip_allocations')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'ipv4': self.ipv4,
            'ipv6_ue': self.ipv6_ue,
            'ipv6_cpe': self.ipv6_cpe,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<IpAllocation {self.device_id}:{self.ipv4}>'

