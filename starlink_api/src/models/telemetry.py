"""
Telemetry-related models for the Starlink Platform API.
"""
from datetime import datetime
from src.models import db
from src.models.base import BaseModel

class UserTerminalTelemetry(db.Model):
    """User Terminal Telemetry model."""
    __tablename__ = 'user_terminal_telemetry'
    
    time = db.Column(db.DateTime, primary_key=True)
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'), primary_key=True)
    downlink_throughput = db.Column(db.Float)
    uplink_throughput = db.Column(db.Float)
    ping_drop_rate_avg = db.Column(db.Float)
    ping_latency_ms_avg = db.Column(db.Float)
    obstruction_percent_time = db.Column(db.Float)
    uptime = db.Column(db.Float)
    signal_quality = db.Column(db.Float)
    active_alerts = db.Column(db.JSON)
    
    # Relationships
    device = db.relationship('Device', back_populates='user_terminal_telemetry')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'time': self.time.isoformat(),
            'device_id': self.device_id,
            'downlink_throughput': self.downlink_throughput,
            'uplink_throughput': self.uplink_throughput,
            'ping_drop_rate_avg': self.ping_drop_rate_avg,
            'ping_latency_ms_avg': self.ping_latency_ms_avg,
            'obstruction_percent_time': self.obstruction_percent_time,
            'uptime': self.uptime,
            'signal_quality': self.signal_quality,
            'active_alerts': self.active_alerts
        }
    
    def __repr__(self):
        return f'<UserTerminalTelemetry {self.device_id}:{self.time}>'


class RouterTelemetry(db.Model):
    """Router Telemetry model."""
    __tablename__ = 'router_telemetry'
    
    time = db.Column(db.DateTime, primary_key=True)
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'), primary_key=True)
    wifi_uptime_s = db.Column(db.Float)
    internet_ping_drop_rate = db.Column(db.Float)
    internet_ping_latency_ms = db.Column(db.Float)
    wifi_pop_ping_drop_rate = db.Column(db.Float)
    wifi_pop_ping_latency_ms = db.Column(db.Float)
    dish_ping_drop_rate = db.Column(db.Float)
    dish_ping_latency_ms = db.Column(db.Float)
    clients = db.Column(db.Integer)
    clients_2ghz = db.Column(db.Integer)
    clients_5ghz = db.Column(db.Integer)
    clients_eth = db.Column(db.Integer)
    wan_tx_bytes = db.Column(db.BigInteger)
    wan_rx_bytes = db.Column(db.BigInteger)
    active_alerts = db.Column(db.JSON)
    
    # Relationships
    device = db.relationship('Device', back_populates='router_telemetry')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'time': self.time.isoformat(),
            'device_id': self.device_id,
            'wifi_uptime_s': self.wifi_uptime_s,
            'internet_ping_drop_rate': self.internet_ping_drop_rate,
            'internet_ping_latency_ms': self.internet_ping_latency_ms,
            'wifi_pop_ping_drop_rate': self.wifi_pop_ping_drop_rate,
            'wifi_pop_ping_latency_ms': self.wifi_pop_ping_latency_ms,
            'dish_ping_drop_rate': self.dish_ping_drop_rate,
            'dish_ping_latency_ms': self.dish_ping_latency_ms,
            'clients': self.clients,
            'clients_2ghz': self.clients_2ghz,
            'clients_5ghz': self.clients_5ghz,
            'clients_eth': self.clients_eth,
            'wan_tx_bytes': self.wan_tx_bytes,
            'wan_rx_bytes': self.wan_rx_bytes,
            'active_alerts': self.active_alerts
        }
    
    def __repr__(self):
        return f'<RouterTelemetry {self.device_id}:{self.time}>'


class Alert(BaseModel):
    """Alert model."""
    __tablename__ = 'alerts'
    
    device_id = db.Column(db.String(36), db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    alert_code = db.Column(db.String(50), nullable=False)
    alert_name = db.Column(db.String(100), nullable=False)
    alert_description = db.Column(db.Text)
    severity = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    device = db.relationship('Device', back_populates='alerts')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'alert_code': self.alert_code,
            'alert_name': self.alert_name,
            'alert_description': self.alert_description,
            'severity': self.severity,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Alert {self.device_id}:{self.alert_code}>'

