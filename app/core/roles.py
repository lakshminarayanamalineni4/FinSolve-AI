from enum import Enum


class Role(str, Enum):
    FINANCE = "finance"
    MARKETING = "marketing"
    HR = "hr"
    ENGINEERING = "engineering"
    C_LEVEL = "c_level"
    EMPLOYEE = "employee"