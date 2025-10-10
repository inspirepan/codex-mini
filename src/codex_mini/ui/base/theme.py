from dataclasses import dataclass
from enum import Enum

from rich.style import Style
from rich.theme import Theme


@dataclass
class Palette:
    red: str
    yellow: str
    green: str
    cyan: str
    blue: str
    orange: str
    grey_blue: str
    grey1: str
    grey2: str
    grey3: str
    purple: str
    diff_add: str
    diff_remove: str
    code_theme: str
    text_background: str


LIGHT_PALETTE = Palette(
    red="red",
    yellow="yellow",
    green="spring_green4",
    cyan="cyan",
    blue="#3678b7",
    orange="#d77757",
    grey_blue="steel_blue",
    grey1="#667e90",
    grey2="#93a4b1",
    grey3="#c4ced4",
    purple="slate_blue3",
    diff_add="#333333 on #69db7c",
    diff_remove="#333333 on #ffa8b4",
    code_theme="ansi_light",
    text_background="#f0f0f0",
)

DARK_PALETTE = Palette(
    red="indian_red",
    yellow="yellow",
    green="sea_green3",
    cyan="cyan",
    blue="dodger_blue1",
    orange="#e6704e",
    grey_blue="steel_blue",
    grey1="#99aabb",
    grey2="gray58",
    grey3="gray30",
    purple="#e7e7ff",
    diff_add="#7fd963",
    diff_remove="#f26d78",
    code_theme="ansi_dark",
    text_background="#373737",
)


class ThemeKey(str, Enum):
    LINES = "lines"
    # DIFF
    DIFF_FILE_NAME = "diff.file_name"
    DIFF_REMOVE = "diff.remove"
    DIFF_ADD = "diff.add"
    DIFF_STATS_ADD = "diff.stats.add"
    DIFF_STATS_REMOVE = "diff.stats.remove"
    # ERROR
    ERROR = "error"
    ERROR_BOLD = "error.bold"
    INTERRUPT = "interrupt"
    # METADATA
    METADATA = "metadata"
    METADATA_DIM = "metadata.dim"
    METADATA_BOLD = "metadata.bold"
    # SPINNER_STATUS
    SPINNER_STATUS = "spinner.status"
    SPINNER_STATUS_BOLD = "spinner.status.bold"
    # STATUS
    STATUS_HINT = "status.hint"
    # USER_INPUT
    USER_INPUT = "user.input"
    USER_INPUT_AT_PATTERN = "user.at_pattern"
    USER_INPUT_SLASH_COMMAND = "user.slash_command"
    # REMINDER
    REMINDER = "reminder"
    REMINDER_BOLD = "reminder.bold"
    # TOOL
    INVALID_TOOL_CALL_ARGS = "tool.invalid_tool_call_args"
    TOOL_NAME = "tool.name"
    TOOL_PARAM_FILE_PATH = "tool.param.file_path"
    TOOL_PARAM = "tool.param"
    TOOL_PARAM_BOLD = "tool.param.bold"
    TOOL_RESULT = "tool.result"
    TOOL_MARK = "tool.mark"
    TOOL_APPROVED = "tool.approved"
    TOOL_REJECTED = "tool.rejected"
    # THINKING
    THINKING = "thinking"
    THINKING_BOLD = "thinking.bold"
    # TODO_ITEM
    TODO_EXPLANATION = "todo.explanation"
    TODO_PENDING_MARK = "todo.pending.mark"
    TODO_COMPLETED_MARK = "todo.completed.mark"
    TODO_IN_PROGRESS_MARK = "todo.in_progress.mark"
    TODO_NEW_COMPLETED_MARK = "todo.new_completed.mark"
    TODO_PENDING = "todo.pending"
    TODO_COMPLETED = "todo.completed"
    TODO_IN_PROGRESS = "todo.in_progress"
    TODO_NEW_COMPLETED = "todo.new_completed"
    # WELCOME
    WELCOME_HIGHLIGHT = "welcome.highlight"
    WELCOME_INFO = "welcome.info"
    # RESUME
    RESUME_FLAG = "resume.flag"
    RESUME_INFO = "resume.info"
    # ANNOTATION
    ANNOTATION_URL = "annotation.url"
    ANNOTATION_URL_HIGHLIGHT = "annotation.url.highlight"
    ANNOTATION_SEARCH_CONTENT = "annotation.search_content"
    # SUB_AGENT
    SUB_AGENT_ORACLE = "sub_agent.oracle"
    # CONFIGURATION DISPLAY
    CONFIG_TABLE_HEADER = "config.table.header"
    CONFIG_STATUS_OK = "config.status.ok"
    CONFIG_STATUS_PRIMARY = "config.status.primary"
    CONFIG_ITEM_NAME = "config.item.name"
    CONFIG_PARAM_LABEL = "config.param.label"
    CONFIG_PANEL_BORDER = "config.panel.border"

    def __str__(self) -> str:
        return self.value


@dataclass
class Themes:
    app_theme: Theme
    markdown_theme: Theme
    code_theme: str
    sub_agent_colors: list[Style]


def get_theme(theme: str | None = None) -> Themes:
    if theme == "light":
        palette = LIGHT_PALETTE
    else:
        palette = DARK_PALETTE
    return Themes(
        app_theme=Theme(
            styles={
                ThemeKey.LINES.value: palette.grey3,
                # DIFF
                ThemeKey.DIFF_FILE_NAME.value: palette.blue,
                ThemeKey.DIFF_REMOVE.value: palette.diff_remove,
                ThemeKey.DIFF_ADD.value: palette.diff_add,
                ThemeKey.DIFF_STATS_ADD.value: palette.green,
                ThemeKey.DIFF_STATS_REMOVE.value: palette.red,
                # ERROR
                ThemeKey.ERROR.value: palette.red,
                ThemeKey.ERROR_BOLD.value: "bold " + palette.red,
                ThemeKey.INTERRUPT.value: "reverse bold " + palette.red,
                # USER_INPUT
                ThemeKey.USER_INPUT.value: palette.cyan + " on " + palette.text_background,
                ThemeKey.USER_INPUT_AT_PATTERN.value: palette.purple + " bold on " + palette.text_background,
                ThemeKey.USER_INPUT_SLASH_COMMAND.value: "bold reverse " + palette.blue,
                # METADATA
                ThemeKey.METADATA.value: palette.grey_blue,
                ThemeKey.METADATA_DIM.value: "dim " + palette.grey_blue,
                ThemeKey.METADATA_BOLD.value: "bold " + palette.grey_blue,
                # SPINNER_STATUS
                ThemeKey.SPINNER_STATUS.value: palette.green,
                ThemeKey.SPINNER_STATUS_BOLD.value: "bold " + palette.green,
                # STATUS
                ThemeKey.STATUS_HINT.value: palette.grey2,
                # REMINDER
                ThemeKey.REMINDER.value: palette.grey1,
                ThemeKey.REMINDER_BOLD.value: "bold " + palette.grey1,
                # TOOL
                ThemeKey.INVALID_TOOL_CALL_ARGS.value: palette.yellow,
                ThemeKey.TOOL_NAME.value: "bold",
                ThemeKey.TOOL_PARAM_FILE_PATH.value: palette.green,
                ThemeKey.TOOL_PARAM.value: palette.green,
                ThemeKey.TOOL_PARAM_BOLD.value: "bold " + palette.green,
                ThemeKey.TOOL_RESULT.value: palette.grey2,
                ThemeKey.TOOL_MARK.value: "bold",
                ThemeKey.TOOL_APPROVED.value: palette.green + " bold reverse",
                ThemeKey.TOOL_REJECTED.value: palette.red + " bold reverse",
                # THINKING
                ThemeKey.THINKING.value: "italic " + palette.grey2,
                ThemeKey.THINKING_BOLD.value: "bold italic " + palette.grey1,
                # TODO_ITEM
                ThemeKey.TODO_EXPLANATION.value: palette.grey1 + " italic",
                ThemeKey.TODO_PENDING_MARK.value: "bold " + palette.grey1,
                ThemeKey.TODO_COMPLETED_MARK.value: "bold " + palette.grey3,
                ThemeKey.TODO_IN_PROGRESS_MARK.value: "bold " + palette.blue,
                ThemeKey.TODO_NEW_COMPLETED_MARK.value: "bold " + palette.green,
                ThemeKey.TODO_PENDING.value: palette.grey1,
                ThemeKey.TODO_COMPLETED.value: palette.grey3 + " strike",
                ThemeKey.TODO_IN_PROGRESS.value: "bold " + palette.blue,
                ThemeKey.TODO_NEW_COMPLETED.value: "bold strike " + palette.green,
                # WELCOME
                ThemeKey.WELCOME_HIGHLIGHT.value: "bold",
                ThemeKey.WELCOME_INFO.value: palette.grey1,
                # RESUME
                ThemeKey.RESUME_FLAG.value: "bold reverse " + palette.green,
                ThemeKey.RESUME_INFO.value: palette.green,
                # URL
                ThemeKey.ANNOTATION_URL.value: palette.blue,
                ThemeKey.ANNOTATION_URL_HIGHLIGHT.value: "bold " + palette.blue,
                ThemeKey.ANNOTATION_SEARCH_CONTENT.value: "italic " + palette.grey2,
                # SUB_AGENT
                ThemeKey.SUB_AGENT_ORACLE.value: palette.orange,
                # CONFIGURATION DISPLAY
                ThemeKey.CONFIG_TABLE_HEADER.value: palette.green,
                ThemeKey.CONFIG_STATUS_OK.value: palette.green,
                ThemeKey.CONFIG_STATUS_PRIMARY.value: palette.yellow,
                ThemeKey.CONFIG_ITEM_NAME.value: palette.cyan,
                ThemeKey.CONFIG_PARAM_LABEL.value: palette.grey1,
                ThemeKey.CONFIG_PANEL_BORDER.value: palette.grey3,
            }
        ),
        markdown_theme=Theme(
            styles={
                "markdown.code": palette.grey1,
                "markdown.h1": "bold reverse",
                "markdown.h1.border": palette.grey3,
                "markdown.h2.border": palette.grey3,
                "markdown.h3": "bold " + palette.grey1,
                "markdown.h4": "bold " + palette.grey2,
                "markdown.item.bullet": palette.grey2,
                "markdown.item.number": palette.grey2,
            }
        ),
        code_theme=palette.code_theme,
        sub_agent_colors=[
            Style(color=palette.yellow),
            Style(color=palette.green),
            Style(color=palette.blue),
            Style(color=palette.purple),
        ],
    )
