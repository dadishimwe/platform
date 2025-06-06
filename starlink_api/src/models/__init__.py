"""
Database models for the Starlink Platform API.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Marshmallow
ma = Marshmallow()

# Import models to ensure they are registered with SQLAlchemy
from src.models.user import User, Role, Permission, RolePermission, UserRole
from src.models.organization import Organization, OrganizationUser, ServicePlan, OrganizationServicePlan
from src.models.device import Device, DeviceConfiguration, DeviceStatus, IpAllocation
from src.models.telemetry import UserTerminalTelemetry, RouterTelemetry, Alert
from src.models.support import Ticket, TicketComment, KbCategory, KbArticle, ChatSession, ChatMessage
from src.models.notification import NotificationTemplate, Notification, AlertConfiguration, AlertNotification, NotificationPreference

