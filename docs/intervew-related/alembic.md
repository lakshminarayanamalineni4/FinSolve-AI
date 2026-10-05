# Step 1 — Install Alembic

## Run:
uv add alembic

## Then initialize it:
    uv run alembic init alembic

## You should get something similar to:
    ds-rpc-01/
    ├── alembic/
    │   ├── versions/
    │   ├── env.py
    │   ├── README
    │   └── script.py.mako
    # Alembic Database Migrations

    Alembic manages schema changes for the FinSolve-AI PostgreSQL database. Migration
    files are stored in `alembic/versions/` and should be committed to source control.

    ## Project Configuration

    Alembic is already included in `pyproject.toml`. The database URL is loaded from
    the application's settings rather than duplicated in `alembic.ini`:

    ```text
    .env -> app.core.config.settings.database_url -> alembic/env.py
    ```

    The `env.py` file must import the declarative base and every model before setting
    `target_metadata`. These imports register the model tables with SQLAlchemy:

    ```python
    from app.core.config import settings
    from app.models.base import Base
    from app.models.permission import Permission
    from app.models.role import Role
    from app.models.role_permission import RolePermission
    from app.models.user import User

    config.set_main_option("sqlalchemy.url", settings.database_url)
    target_metadata = Base.metadata
    ```

    Keep `sqlalchemy.url` in `alembic.ini` as a placeholder. `env.py` replaces it at
    runtime with the value from the environment.

    ## Create a Migration

    Run these commands from the project root:

    ```bash
    uv run alembic revision --autogenerate -m "describe the schema change"
    ```

    Autogenerate compares the imported SQLAlchemy models with the current database
    schema. It does not replace a manual review. Open the new file in
    `alembic/versions/` and verify the table, column, index, constraint, and foreign
    key operations before applying it.

    For the initial RBAC migration, the expected tables are:

    - `users`
    - `roles`
    - `permissions`
    - `role_permissions`

    ## Apply Migrations

    Apply all unapplied migrations:

    ```bash
    uv run alembic upgrade head
    ```

    Check the current database revision and available migration history with:

    ```bash
    uv run alembic current
    uv run alembic history
    ```

    To downgrade one revision during local development:

    ```bash
    uv run alembic downgrade -1
    ```

    ## Troubleshooting

    If autogenerate reports that `env.py` does not provide a `MetaData` object,
    confirm that:

    1. `Base` is imported from `app.models.base`.
    2. Every model is imported in `alembic/env.py` before `Base.metadata` is read.
    3. `target_metadata = Base.metadata` is present and is not set to `None`.
    4. The database URL in `.env` is valid and the PostgreSQL database is reachable.

    Never edit an already-applied migration. Create a new migration for subsequent
    schema changes.