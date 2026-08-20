from enum import Enum


class ResourceCategory(str, Enum):
    FINANCE = "finance"
    MARKETING = "marketing"
    HR = "hr"
    ENGINEERING = "engineering"
    GENERAL = "general"