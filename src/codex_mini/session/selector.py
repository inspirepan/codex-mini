import time
from typing import TYPE_CHECKING

from codex_mini.trace import log, log_debug

if TYPE_CHECKING:
    from questionary import Choice

from .session import Session


def resume_select_session() -> str | None:
    sessions = Session.list()
    if not sessions:
        log("No sessions found for this project.")
        return None

    def _fmt(ts: float) -> str:
        try:
            return time.strftime("%m-%d %H:%M:%S", time.localtime(ts))
        except Exception:
            return str(ts)

    try:
        import questionary

        choices: list[Choice] = []
        for s in sessions:
            first_user_message = s.first_user_message or "N/A"
            msg_count_display = "N/A" if s.messages_count == -1 else str(s.messages_count)
            model_display = s.model_name or "N/A"

            title = [
                ("class:d", f"{_fmt(s.created_at):<16} "),
                ("class:d", f"{_fmt(s.updated_at):<16} "),
                ("class:b", f"{msg_count_display:>3}  "),
                (
                    "class:t",
                    f"{model_display[:14] + '…' if len(model_display) > 14 else model_display:<15}  ",
                ),
                (
                    "class:t",
                    f"{first_user_message.strip().replace('\n', ' ↩ '):<50}",
                ),
            ]
            choices.append(questionary.Choice(title=title, value=s.id))
        return questionary.select(
            message=f"{' Created at':<17} {'Updated at':<16} {'Msg':>3}  {'Model':<15}  {'First message':<50}",
            choices=choices,
            pointer="→",
            instruction="↑↓ to move",
            style=questionary.Style(
                [
                    ("t", ""),
                    ("b", "bold"),
                    ("d", "dim"),
                ]
            ),
        ).ask()
    except Exception as e:
        log_debug(f"Failed to use questionary for session select, {e}")

        for i, s in enumerate(sessions, 1):
            msg_count_display = "N/A" if s.messages_count == -1 else str(s.messages_count)
            model_display = s.model_name or "N/A"
            print(
                f"{i}. {_fmt(s.updated_at)}  {msg_count_display:>3} "
                f"{model_display[:14] + '…' if len(model_display) > 14 else model_display:<15} {s.id}  {s.work_dir}"
            )
        try:
            raw = input("Select a session number: ").strip()
            idx = int(raw)
            if 1 <= idx <= len(sessions):
                return str(sessions[idx - 1].id)
        except Exception:
            return None
    return None
