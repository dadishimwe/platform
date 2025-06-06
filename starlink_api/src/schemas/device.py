"""
Device-related schemas for the Starlink Platform API.
"""
from marshmallow import fields
from src.models import ma
from src.models.device import Device, DeviceConfiguration, DeviceStatus, IpAllocation

class DeviceSchema(ma.SQLAlchemySchema):
    """Device schema."""
    class Meta:
        model = Device
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    device_id = fields.String(required=True)
    device_type = fields.String(required=True)
    organization_id = fields.String(required=True)
    name = fields.String()
    description = fields.String()
    location = fields.String()
    h3_cell_id = fields.String()
    software_version = fields.String()
    hardware_version = fields.String()
    last_seen = fields.DateTime()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class DeviceConfigurationSchema(ma.SQLAlchemySchema):
    """Device Configuration schema."""
    class Meta:
        model = DeviceConfiguration
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    device_id = fields.String(required=True)
    config_key = fields.String(required=True)
    config_value = fields.Dict(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class DeviceStatusSchema(ma.SQLAlchemySchema):
    """Device Status schema."""
    class Meta:
        model = DeviceStatus
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    device_id = fields.String(required=True)
    status = fields.String(required=True)
    details = fields.Dict()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class IpAllocationSchema(ma.SQLAlchemySchema):
    """IP Allocation schema."""
    class Meta:
        model = IpAllocation
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    device_id = fields.String(required=True)
    ipv4 = fields.String()
    ipv6_ue = fields.String()
    ipv6_cpe = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Initialize schemas
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)
device_configuration_schema = DeviceConfigurationSchema()
device_configurations_schema = DeviceConfigurationSchema(many=True)
device_status_schema = DeviceStatusSchema()
device_statuses_schema = DeviceStatusSchema(many=True)
ip_allocation_schema = IpAllocationSchema()
ip_allocations_schema = IpAllocationSchema(many=True)

