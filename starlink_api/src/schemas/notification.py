"""
Notification-related schemas for the Starlink Platform API.
"""
from marshmallow import fields
from src.models import ma
from src.models.notification import NotificationTemplate, Notification, AlertConfiguration, AlertNotification, NotificationPreference

class NotificationTemplateSchema(ma.SQLAlchemySchema):
    """Notification Template schema."""
    class Meta:
        model = NotificationTemplate
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    name = fields.String(required=True)
    subject = fields.String(required=True)
    content = fields.String(required=True)
    type = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class NotificationSchema(ma.SQLAlchemySchema):
    """Notification schema."""
    class Meta:
        model = Notification
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    user_id = fields.String(required=True)
    template_id = fields.String(required=True)
    data = fields.Dict()
    is_read = fields.Boolean()
    read_at = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)


class AlertConfigurationSchema(ma.SQLAlchemySchema):
    """Alert Configuration schema."""
    class Meta:
        model = AlertConfiguration
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    organization_id = fields.String(required=True)
    device_id = fields.String()
    alert_type = fields.String(required=True)
    threshold = fields.Float()
    comparison = fields.String(required=True)
    enabled = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class AlertNotificationSchema(ma.SQLAlchemySchema):
    """Alert Notification schema."""
    class Meta:
        model = AlertNotification
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    alert_config_id = fields.String(required=True)
    device_id = fields.String(required=True)
    value = fields.Float()
    triggered_at = fields.DateTime(required=True)
    resolved_at = fields.DateTime()
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class NotificationPreferenceSchema(ma.SQLAlchemySchema):
    """Notification Preference schema."""
    class Meta:
        model = NotificationPreference
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    user_id = fields.String(required=True)
    notification_type = fields.String(required=True)
    email_enabled = fields.Boolean()
    push_enabled = fields.Boolean()
    in_app_enabled = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Initialize schemas
notification_template_schema = NotificationTemplateSchema()
notification_templates_schema = NotificationTemplateSchema(many=True)
notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)
alert_configuration_schema = AlertConfigurationSchema()
alert_configurations_schema = AlertConfigurationSchema(many=True)
alert_notification_schema = AlertNotificationSchema()
alert_notifications_schema = AlertNotificationSchema(many=True)
notification_preference_schema = NotificationPreferenceSchema()
notification_preferences_schema = NotificationPreferenceSchema(many=True)

