"""
Database initialization script for the Starlink Platform API.
"""
from werkzeug.security import generate_password_hash
from src.models import db
from src.models.user import User, Role, Permission, UserRole, RolePermission

def init_roles_and_permissions():
    """
    Initialize roles and permissions in the database.
    """
    print("Initializing roles and permissions...")
    
    # Create roles
    roles = {
        'Super Admin': 'Full access to all features',
        'Admin': 'Administrative access to manage organizations and users',
        'Organization Admin': 'Administrative access within an organization',
        'Technician': 'Access to device management and technical operations',
        'Support': 'Access to support features',
        'Viewer': 'Read-only access',
        'Client': 'Client access to their own data'
    }
    
    role_objects = {}
    for name, description in roles.items():
        role = Role.query.filter_by(name=name).first()
        if not role:
            role = Role(name=name, description=description)
            db.session.add(role)
            print(f"Created role: {name}")
        role_objects[name] = role
    
    # Create permissions
    permissions = [
        # User management
        ('user', 'create'),
        ('user', 'read'),
        ('user', 'update'),
        ('user', 'delete'),
        
        # Organization management
        ('organization', 'create'),
        ('organization', 'read'),
        ('organization', 'update'),
        ('organization', 'delete'),
        
        # Device management
        ('device', 'create'),
        ('device', 'read'),
        ('device', 'update'),
        ('device', 'delete'),
        
        # Telemetry
        ('telemetry', 'read'),
        ('telemetry', 'sync'),
        
        # Support
        ('support', 'create'),
        ('support', 'read'),
        ('support', 'update'),
        ('support', 'delete'),
        
        # Notification
        ('notification', 'create'),
        ('notification', 'read'),
        ('notification', 'update'),
        ('notification', 'delete'),
    ]
    
    permission_objects = {}
    for resource, action in permissions:
        permission = Permission.query.filter_by(resource=resource, action=action).first()
        if not permission:
            permission = Permission(resource=resource, action=action)
            db.session.add(permission)
            print(f"Created permission: {resource}.{action}")
        permission_objects[f"{resource}.{action}"] = permission
    
    # Commit to get IDs
    db.session.commit()
    
    # Assign permissions to roles
    role_permissions = {
        'Super Admin': [f"{resource}.{action}" for resource, action in permissions],
        'Admin': [
            'user.create', 'user.read', 'user.update', 'user.delete',
            'organization.create', 'organization.read', 'organization.update', 'organization.delete',
            'device.read', 'telemetry.read',
            'support.read', 'support.update',
            'notification.read', 'notification.update'
        ],
        'Organization Admin': [
            'user.create', 'user.read', 'user.update',
            'organization.read', 'organization.update',
            'device.create', 'device.read', 'device.update',
            'telemetry.read',
            'support.create', 'support.read', 'support.update',
            'notification.read', 'notification.update'
        ],
        'Technician': [
            'device.read', 'device.update',
            'telemetry.read', 'telemetry.sync',
            'support.create', 'support.read', 'support.update'
        ],
        'Support': [
            'user.read',
            'organization.read',
            'device.read',
            'telemetry.read',
            'support.create', 'support.read', 'support.update'
        ],
        'Viewer': [
            'user.read',
            'organization.read',
            'device.read',
            'telemetry.read',
            'support.read',
            'notification.read'
        ],
        'Client': [
            'device.read',
            'telemetry.read',
            'support.create', 'support.read',
            'notification.read'
        ]
    }
    
    # Clear existing role permissions
    RolePermission.query.delete()
    
    # Assign permissions to roles
    for role_name, permission_keys in role_permissions.items():
        role = role_objects[role_name]
        for permission_key in permission_keys:
            permission = permission_objects[permission_key]
            role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
            db.session.add(role_permission)
            print(f"Assigned permission {permission_key} to role {role_name}")
    
    # Commit changes
    db.session.commit()
    print("Roles and permissions initialized successfully")

def create_admin_user(email, password, first_name='Admin', last_name='User'):
    """
    Create an admin user if it doesn't exist.
    """
    print(f"Creating admin user: {email}")
    
    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        print(f"User {email} already exists")
        return user
    
    # Create user
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    
    # Assign Super Admin role
    super_admin_role = Role.query.filter_by(name='Super Admin').first()
    if super_admin_role:
        user_role = UserRole(user_id=user.id, role_id=super_admin_role.id)
        db.session.add(user_role)
        db.session.commit()
    
    print(f"Admin user {email} created successfully")
    return user

def init_db():
    """
    Initialize the database with default data.
    """
    print("Initializing database...")
    
    # Create tables
    db.create_all()
    
    # Initialize roles and permissions
    init_roles_and_permissions()
    
    # Create admin user
    create_admin_user('admin@example.com', 'adminpassword')
    
    print("Database initialization completed")

