import logging

from app.core.config import settings

def setup_logging() -> None:
    logging.basicConfig( # configures Python's root logger
        level=getattr(logging, settings.log_level.upper()), # returns the corresponding logging level
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", # 2026-08-19 08:30:12 | INFO | app.main | Application started
    )