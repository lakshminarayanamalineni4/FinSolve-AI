from app.core.database import session_scope
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User


ROLES = {
    "finance"       : "Finance team role",
    "marketing"     : "Marketing team role",
    "hr"            : "HR team role",
    "engineering"   : "Engineering team role",
    "c_level"       : "C-Level executive role",
    "employee"      : "General employee role",
}


PERMISSIONS = {
    "read_finance"      : "Read finance resources",
    "read_marketing"    : "Read marketing resources",
    "read_hr"           : "Read HR resources",
    "read_engineering"  : "Read engineering resources",
    "read_general"      : "Read general company resources",
}


ROLE_PERMISSIONS = {
    "finance"       : ["read_finance", "read_general"],
    "marketing"     : ["read_marketing", "read_general"],
    "hr"            : ["read_hr", "read_general"],
    "engineering"   : ["read_engineering", "read_general"],
    "employee"      : ["read_general"],
    "c_level"       : [
        "read_finance",
        "read_marketing",
        "read_hr",
        "read_engineering",
        "read_general",
    ],
}


def seed_roles(db):
    roles = {}

    for name, description in ROLES.items():
        role = db.query(Role).filter(Role.name == name).first()

        if role is None:
            role = Role(
                name=name,
                description=description,
            )
            db.add(role)
            db.flush()

        roles[name] = role

    return roles


def seed_permissions(db):
    permissions = {}

    for name, description in PERMISSIONS.items():
        permission = (
            db.query(Permission)
            .filter(Permission.name == name)
            .first()
        )

        if permission is None:
            permission = Permission(
                name=name,
                description=description,
            )
            db.add(permission)
            db.flush()

        permissions[name] = permission

    return permissions


def seed_role_permissions(db, roles, permissions):
    for role_name, permission_names in ROLE_PERMISSIONS.items():
        role = roles[role_name]

        for permission_name in permission_names:
            permission = permissions[permission_name]

            existing_mapping = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == permission.id,
                )
                .first()
            )

            if existing_mapping is None:
                db.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id,
                    )
                )


def main():
    with session_scope() as db:
        roles = seed_roles(db)
        permissions = seed_permissions(db)

        seed_role_permissions(
            db,
            roles,
            permissions,
        )

        db.commit()

        print("RBAC seed completed successfully.")
        print(f"Roles: {len(roles)}")
        print(f"Permissions: {len(permissions)}")
        print("Role-permission mappings: 14")

        
if __name__ == "__main__":
    main()

# uv run python -m app.scripts.seed_rbac