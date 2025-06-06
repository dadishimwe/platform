"""
Telemetry-related schemas for the Starlink Platform API.
"""
from marshmallow import fields
from src.models import ma
from src.models.telemetry import UserTerminalTelemetry, RouterTelemetry, Alert

class UserTerminalTelemetrySchema(ma.SQLAlchemySchema):
    """User Terminal Telemetry schema."""
    class Meta:
        model = UserTerminalTelemetry
        load_instance = True
    
    time = fields.DateTime(required=True)
    device_id = fields.String(required=True)
    downlink_throughput = fields.Float()
    uplink_throughput = fields.Float()
    ping_drop_rate_avg = fields.Float()
    ping_latency_ms_avg = fields.Float()
    obstruction_percent_time = fields.Float()
    uptime = fields.Float()
    signal_quality = fields.Float()
    active_alerts = fields.List(fields.Integer())


class RouterTelemetrySchema(ma.SQLAlchemySchema):
    """Router Telemetry schema."""
    class Meta:
        model = RouterTelemetry
        load_instance = True
    
    time = fields.DateTime(required=True)
    device_id = fields.String(required=True)
    wifi_uptime_s = fields.Float()
    internet_ping_drop_rate = fields.Float()
    internet_ping_latency_ms = fields.Float()
    wifi_pop_ping_drop_rate = fields.Float()
    wifi_pop_ping_latency_ms = fields.Float()
    dish_ping_drop_rate = fields.Float()
    dish_ping_latency_ms = fields.Float()
    clients = fields.Integer()
    clients_2ghz = fields.Integer()
    clients_5ghz = fields.Integer()
    clients_eth = fields.Integer()
    wan_tx_bytes = fields.Integer()
    wan_rx_bytes = fields.Integer()
    active_alerts = fields.List(fields.Integer())


class AlertSchema(ma.SQLAlchemySchema):
    """Alert schema."""
    class Meta:
        model = Alert
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    device_id = fields.String(required=True)
    alert_code = fields.String(required=True)
    alert_name = fields.String(required=True)
    alert_description = fields.String()
    severity = fields.String(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Initialize schemas
user_terminal_telemetry_schema = UserTerminalTelemetrySchema()
user_terminal_telemetries_schema = UserTerminalTelemetrySchema(many=True)
router_telemetry_schema = RouterTelemetrySchema()
router_telemetries_schema = RouterTelemetrySchema(many=True)
alert_schema = AlertSchema()
alerts_schema = AlertSchema(many=True)

