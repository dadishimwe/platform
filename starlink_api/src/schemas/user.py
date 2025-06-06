"""
User-related schemas for the Starlink Platform API.
"""
from marshmallow import Schema, fields, validate, post_load
from src.models import ma
from src.models.user import User, Role, Permission, RolePermission, UserRole

class UserSchema(ma.SQLAlchemySchema):
    """User schema."""
    class Meta:
        model = User
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8))
    first_name = fields.String()
    last_name = fields.String()
    phone = fields.String()
    last_login = fields.DateTime(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    is_verified = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserUpdateSchema(ma.SQLAlchemySchema):
    """User update schema."""
    class Meta:
        model = User
        load_instance = True
        partial = True
    
    email = fields.Email()
    password = fields.String(load_only=True, validate=validate.Length(min=8))
    first_name = fields.String()
    last_name = fields.String()
    phone = fields.String()


class RoleSchema(ma.SQLAlchemySchema):
    """Role schema."""
    class Meta:
        model = Role
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PermissionSchema(ma.SQLAlchemySchema):
    """Permission schema."""
    class Meta:
        model = Permission
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    resource = fields.String(required=True)
    action = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class RolePermissionSchema(ma.SQLAlchemySchema):
    """Role-Permission association schema."""
    class Meta:
        model = RolePermission
        load_instance = True
    
    role_id = fields.String(required=True)
    permission_id = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)


class UserRoleSchema(ma.SQLAlchemySchema):
    """User-Role association schema."""
    class Meta:
        model = UserRole
        load_instance = True
    
    user_id = fields.String(required=True)
    role_id = fields.String(required=True)
    organization_id = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)


class LoginSchema(Schema):
    """Login schema."""
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TokenSchema(Schema):
    """Token schema."""
    access_token = fields.String()
    refresh_token = fields.String()
    token_type = fields.String()
    expires_in = fields.Integer()


# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserUpdateSchema()
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)
role_permission_schema = RolePermissionSchema()
role_permissions_schema = RolePermissionSchema(many=True)
user_role_schema = UserRoleSchema()
user_roles_schema = UserRoleSchema(many=True)
login_schema = LoginSchema()
token_schema = TokenSchema()

