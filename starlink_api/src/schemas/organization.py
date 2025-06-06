"""
Organization-related schemas for the Starlink Platform API.
"""
from marshmallow import fields
from src.models import ma
from src.models.organization import Organization, OrganizationUser, ServicePlan, OrganizationServicePlan

class OrganizationSchema(ma.SQLAlchemySchema):
    """Organization schema."""
    class Meta:
        model = Organization
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    address = fields.String()
    city = fields.String()
    state = fields.String()
    country = fields.String()
    postal_code = fields.String()
    phone = fields.String()
    email = fields.Email()
    website = fields.URL()
    logo_url = fields.URL()
    parent_id = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OrganizationUserSchema(ma.SQLAlchemySchema):
    """Organization-User association schema."""
    class Meta:
        model = OrganizationUser
        load_instance = True
    
    organization_id = fields.String(required=True)
    user_id = fields.String(required=True)
    role = fields.String(required=True)
    is_primary = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ServicePlanSchema(ma.SQLAlchemySchema):
    """Service Plan schema."""
    class Meta:
        model = ServicePlan
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    data_limit_gb = fields.Float()
    speed_limit_mbps = fields.Float()
    price = fields.Float()
    currency = fields.String()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OrganizationServicePlanSchema(ma.SQLAlchemySchema):
    """Organization-ServicePlan association schema."""
    class Meta:
        model = OrganizationServicePlan
        load_instance = True
    
    organization_id = fields.String(required=True)
    service_plan_id = fields.String(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Initialize schemas
organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)
organization_user_schema = OrganizationUserSchema()
organization_users_schema = OrganizationUserSchema(many=True)
service_plan_schema = ServicePlanSchema()
service_plans_schema = ServicePlanSchema(many=True)
organization_service_plan_schema = OrganizationServicePlanSchema()
organization_service_plans_schema = OrganizationServicePlanSchema(many=True)

