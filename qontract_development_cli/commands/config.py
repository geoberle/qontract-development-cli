import logging
import subprocess

import typer
from rich.prompt import Prompt

from ..config import config, user_config_file
from ..models import DEFAULT_PROFILE, Env
from ..utils import console

app = typer.Typer()
log = logging.getLogger(__name__)


@app.command()
def init():
    """Dump default files (config, environment, profiles)"""
    # qontract-development config
    config.save()
    console.print(f"Config file '[b]{user_config_file}[/]' saved.\n")

    # dev env
    console.print("Creating 'dev' environment ...")
    env = Env(name="dev")
    env.settings.app_interface_path = Prompt.ask(
        "local app-interface path",
        default=str(env.settings.app_interface_path),
        console=console,
    )
    console.print()
    env.settings.config = Prompt.ask(
        "app-interface config",
        default=str(env.settings.config),
        console=console,
    )
    env.dump()
    console.print()
    console.print(f"Environment file '[b]{env.name}[/]' saved.\n")

    # default profile
    console.print("Creating defaults profile ...")
    DEFAULT_PROFILE.settings.qontract_reconcile_path = Prompt.ask(
        "local qontract-reconcile path",
        default=str(DEFAULT_PROFILE.settings.qontract_reconcile_path),
        console=console,
    )
    console.print()
    DEFAULT_PROFILE.settings.qontract_schemas_path = Prompt.ask(
        "local qontract-schemas path",
        default=str(DEFAULT_PROFILE.settings.qontract_schemas_path),
        console=console,
    )
    console.print()
    DEFAULT_PROFILE.settings.qontract_server_path = Prompt.ask(
        "local qontract-server path",
        default=str(DEFAULT_PROFILE.settings.qontract_server_path),
        console=console,
    )
    DEFAULT_PROFILE.dump()
    console.print()
    console.print(f"Defaults profile file '[b]{DEFAULT_PROFILE.name}[/]' saved.")


@app.command()
def edit():
    """Edit config in your editor."""
    console.print(f"Opening [b]{user_config_file}[/] in your editor ...")
    subprocess.run([config.editor, user_config_file])
