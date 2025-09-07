from datetime import datetime

from rich.console import Console
from rich.text import Text

log_console = Console()

_debug_write_to_file = True
_debug_log_file = "debug.log"


def log(*objects: str | tuple[str, str], style: str = ""):
    log_console.print(
        *((Text(obj[0], style=obj[1]) if isinstance(obj, tuple) else Text(obj)) for obj in objects), style=style
    )


def log_debug(*objects: str | tuple[str, str], style: str = "blue"):
    if _debug_write_to_file:
        message_parts = []
        for obj in objects:
            if isinstance(obj, tuple):
                message_parts.append(obj[0])  # type: ignore
            else:
                message_parts.append(obj)  # type: ignore
        message = " ".join(message_parts)  # type: ignore
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(_debug_log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    else:
        log_console.print(
            *((Text(obj[0], style=obj[1]) if isinstance(obj, tuple) else Text(obj)) for obj in objects), style=style
        )
