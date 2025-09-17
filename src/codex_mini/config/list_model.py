from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from codex_mini.config import Config
from codex_mini.ui.theme import ThemeKey, get_theme


def mask_api_key(api_key: str | None) -> str:
    """Mask API key to show only first 6 and last 6 characters with *** in between"""
    if not api_key or api_key == "N/A":
        return "N/A"

    if len(api_key) <= 12:
        return api_key

    return f"{api_key[:6]} … {api_key[-6:]}"


def display_models_and_providers(config: Config):
    """Display models and providers configuration using rich formatting"""
    themes = get_theme(config.theme)
    console = Console(theme=themes.app_theme)

    # Display providers section
    providers_table = Table.grid(padding=(0, 1), expand=True)
    providers_table.add_column(width=2, no_wrap=True)  # Status
    providers_table.add_column(overflow="fold")  # Name
    providers_table.add_column(overflow="fold")  # Protocol
    providers_table.add_column(overflow="fold")  # Base URL
    providers_table.add_column(overflow="fold")  # API Key

    # Add header
    providers_table.add_row(
        Text("", style="bold"),
        Text("Name", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
        Text("Protocol", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
        Text("Base URL", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
        Text("API Key", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
    )

    # Add providers
    for provider in config.provider_list:
        status = Text("✔", style=f"bold {ThemeKey.CONFIG_STATUS_OK}")
        name = Text(provider.provider_name, style=ThemeKey.CONFIG_ITEM_NAME)
        protocol = Text(str(provider.protocol.value), style="")
        base_url = Text(provider.base_url or "N/A", style="")
        api_key = Text(mask_api_key(provider.api_key), style="")

        providers_table.add_row(status, name, protocol, base_url, api_key)

    # Display models section
    models_table = Table.grid(padding=(0, 1), expand=True)
    models_table.add_column(width=2, no_wrap=True)  # Status
    models_table.add_column(overflow="fold", ratio=1)  # Name
    models_table.add_column(overflow="fold", ratio=2)  # Model
    models_table.add_column(overflow="fold", ratio=2)  # Provider
    models_table.add_column(overflow="fold", ratio=3)  # Params

    # Add header
    models_table.add_row(
        Text("", style="bold"),
        Text("Name", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
        Text("Model", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
        Text("Provider", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
        Text("Params", style=f"bold {ThemeKey.CONFIG_TABLE_HEADER}"),
    )

    # Add models
    for model in config.model_list:
        status = Text("✔", style=f"bold {ThemeKey.CONFIG_STATUS_OK}")
        if model.model_name == config.main_model:
            status = Text("★", style=f"bold {ThemeKey.CONFIG_STATUS_PRIMARY}")  # Mark main model

        name = Text(
            model.model_name,
            style=ThemeKey.CONFIG_STATUS_PRIMARY
            if model.model_name == config.main_model
            else ThemeKey.CONFIG_ITEM_NAME,
        )
        model_name = Text(model.model_params.model or "N/A", style="")
        provider = Text(model.provider, style="")
        params: list[Text] = []
        if model.model_params.reasoning:
            params.append(
                Text.assemble(("reason-effort", ThemeKey.CONFIG_PARAM_LABEL), ": ", model.model_params.reasoning.effort)
            )
            if model.model_params.reasoning.summary is not None:
                params.append(
                    Text.assemble(
                        ("reason-summary", ThemeKey.CONFIG_PARAM_LABEL),
                        ": ",
                        model.model_params.reasoning.summary,
                    )
                )
        if model.model_params.verbosity:
            params.append(Text.assemble(("verbosity", ThemeKey.CONFIG_PARAM_LABEL), ": ", model.model_params.verbosity))
        if model.model_params.thinking:
            params.append(
                Text.assemble(
                    ("thinking-budget-tokens", ThemeKey.CONFIG_PARAM_LABEL),
                    ": ",
                    str(model.model_params.thinking.budget_tokens or "N/A"),
                )
            )
        if model.model_params.provider_routing:
            params.append(
                Text.assemble(
                    ("provider-routing", ThemeKey.CONFIG_PARAM_LABEL),
                    ": ",
                    model.model_params.provider_routing.model_dump_json(exclude_none=True),
                )
            )
        if model.model_params.plugins:
            params.append(
                Text.assemble(
                    ("plugins", ThemeKey.CONFIG_PARAM_LABEL),
                    ": ",
                    ", ".join([p.id for p in model.model_params.plugins]),
                )
            )
        if len(params) == 0:
            params.append(Text("N/A", style=ThemeKey.CONFIG_PARAM_LABEL))
        models_table.add_row(status, name, model_name, provider, Group(*params))

    # Create panels and display
    providers_panel = Panel(
        providers_table,
        title=Text("Providers Configuration", style="white bold"),
        border_style=ThemeKey.CONFIG_PANEL_BORDER,
        padding=(0, 1),
        title_align="left",
    )

    models_panel = Panel(
        models_table,
        title=Text("Models Configuration", style="white bold"),
        border_style=ThemeKey.CONFIG_PANEL_BORDER,
        padding=(0, 1),
        title_align="left",
    )

    console.print(providers_panel)
    console.print()
    console.print(models_panel)

    # Display main model info
    console.print()
    console.print(Text.assemble(("Default Model: ", "bold"), (config.main_model, ThemeKey.CONFIG_STATUS_PRIMARY)))

    # Display task model if configured
    if config.task_model:
        console.print(Text.assemble(("Task Model: ", "bold"), (config.task_model, ThemeKey.CONFIG_STATUS_PRIMARY)))

    # Display plan model if configured
    if config.plan_model:
        console.print(Text.assemble(("Plan Model: ", "bold"), (config.plan_model, ThemeKey.CONFIG_STATUS_PRIMARY)))

    # Display task model if configured
    if config.task_model:
        console.print(Text.assemble(("Task Model: ", "bold"), (config.task_model, ThemeKey.CONFIG_STATUS_PRIMARY)))

    # Display oracle model if configured
    if config.oracle_model:
        console.print(Text.assemble(("Oracle Model: ", "bold"), (config.oracle_model, ThemeKey.CONFIG_STATUS_PRIMARY)))
