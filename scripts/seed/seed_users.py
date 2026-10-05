from sqlalchemy import select

from app.core.database import session_scope
from app.core.security import hash_mobile, hash_password, encrypt_mobile
from app.models.role import Role
from app.models.user import User
from app.models.role_permission import RolePermission
from app.models.permission import Permission

USERS = [
    {
        "username": "Tony",
        "password": "password123",
        "mobile": "9876543210",
        "role": "engineering",
    },
    {
        "username": "Bruce",
        "password": "securepass",
        "mobile": "9876543211",
        "role": "marketing",
    },
    {
        "username": "Sam",
        "password": "financepass",
        "mobile": "9876543212",
        "role": "finance",
    },
    {
        "username": "Peter",
        "password": "pete123",
        "mobile": "9876543213",
        "role": "engineering",
    },
    {
        "username": "Sid",
        "password": "sidpass123",
        "mobile": "9876543214",
        "role": "marketing",
    },
    {
        "username": "Natasha",
        "password": "hrpass123",
        "mobile": "9876543215",
        "role": "hr",
    },
    {
        "username": "Alex",
        "password": "Alex123",
        "mobile": "9876543216",
        "role": "c_level"
    },
    {
        "username": "Pedro",
        "password": "Pedro123",
        "mobile": "9876543217",
        "role": "employee"
    }
]


def seed_users() -> None:
    with session_scope() as db:
        for user_data in USERS:

            existing_user = db.scalar(
                select(User).where(
                    User.username == user_data["username"]
                )
            )

            if existing_user:
                print(
                    f"User '{user_data['username']}' already exists. "
                    "Skipping."
                )
                continue

            role = db.scalar(
                select(Role).where(
                    Role.name == user_data["role"]
                )
            )

            if role is None:
                raise ValueError(
                    f"Role '{user_data['role']}' does not exist."
                )

            user = User(
                username=user_data["username"],
                password_hash=hash_password(user_data["password"]),
                mobile_encrypted=encrypt_mobile(
                    user_data["mobile"]
                ),
                mobile_hash=hash_mobile(
                    user_data["mobile"]
                ),
                role_id=role.id,
                is_active=True,
            )

            db.add(user)

        db.commit()

    print("User seeding completed.")


if __name__ == "__main__":
    seed_users()

# uv run python -m app.scripts.seed_users