import logging
from typing import Optional, Iterable

from config import Config
from pyrogram import Client
from rich.console import Console
from rich.table import Table
from pyromod import listen
from pyromod.types.identifier import Identifier

API_ID: int = Config.API_ID
API_HASH: str = Config.API_HASH
BOT_TOKEN: str = Config.BOT_TOKEN
START_PIC: Optional[str] = Config.START_PIC

LOG = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("HackBot")

def _identifier_field_names() -> Iterable[str]:
    dataclass_fields = getattr(Identifier, "__dataclass_fields__", None)
    if dataclass_fields:
        return dataclass_fields.keys()
    annotations = getattr(Identifier, "__annotations__", None)
    if annotations:
        return annotations.keys()
    annotate_func = getattr(Identifier, "__annotate_func__", None)
    if annotate_func:
        try:
            annotations = annotate_func()
        except TypeError:
            annotations = annotate_func
        if isinstance(annotations, dict):
            return annotations.keys()
    return ()


def _identifier_matches(self: Identifier, update: Identifier) -> bool:
    for field in _identifier_field_names():
        pattern_value = getattr(self, field)
        update_value = getattr(update, field)

        if pattern_value is not None:
            if isinstance(update_value, list):
                if isinstance(pattern_value, list):
                    if not set(update_value).intersection(set(pattern_value)):
                        return False
                elif pattern_value not in update_value:
                    return False
            elif isinstance(pattern_value, list):
                if update_value not in pattern_value:
                    return False
            elif update_value != pattern_value:
                return False
    return True


def _identifier_count_populated(self: Identifier) -> int:
    non_null_count = 0
    for field in _identifier_field_names():
        if getattr(self, field) is not None:
            non_null_count += 1
    return non_null_count


if not getattr(Identifier, "__annotations__", None):
    Identifier.__annotations__ = {}

Identifier.matches = _identifier_matches
Identifier.count_populated = _identifier_count_populated

# === Pyrogram Client ===
app = Client(
    "Hack",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Export
__all__ = ["app", "LOG", "logger", "START_PIC"]
