from enum import Enum

from app.core.roles import Role
from app.core.resources import ResourceCategory


class Permission(str, Enum):
    READ_FINANCE = "read_finance"
    READ_MARKETING = "read_marketing"
    READ_HR = "read_hr"
    READ_ENGINEERING = "read_engineering"
    READ_GENERAL = "read_general"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.FINANCE: {
        Permission.READ_FINANCE,
        Permission.READ_GENERAL,
    },
    Role.MARKETING: {
        Permission.READ_MARKETING,
        Permission.READ_GENERAL,
    },
    Role.HR: {
        Permission.READ_HR,
        Permission.READ_GENERAL,
    },
    Role.ENGINEERING: {
        Permission.READ_ENGINEERING,
        Permission.READ_GENERAL,
    },
    Role.C_LEVEL: {
        Permission.READ_FINANCE,
        Permission.READ_MARKETING,
        Permission.READ_HR,
        Permission.READ_ENGINEERING,
        Permission.READ_GENERAL,
    },
    Role.EMPLOYEE: {
        Permission.READ_GENERAL,
    },
}

PERMISSION_RESOURCES = {
    Permission.READ_FINANCE: {
        ResourceCategory.FINANCE,
    },
    Permission.READ_MARKETING: {
        ResourceCategory.MARKETING,
    },
    Permission.READ_HR: {
        ResourceCategory.HR,
    },
    Permission.READ_ENGINEERING: {
        ResourceCategory.ENGINEERING,
    },
    Permission.READ_GENERAL: {
        ResourceCategory.GENERAL,
    },
}