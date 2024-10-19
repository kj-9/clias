import os
import sys
from dataclasses import dataclass
from pathlib import Path

import click
import yaml  # type: ignore
from jinja2 import Template

from clier.run import run_command


@dataclass
class ClickFuncArgs:
    arg: list[str]
    kwargs: dict[str, str]


@dataclass
class CommandSpec:
    name: str
    help: str
    shell: str
    arguments: list[ClickFuncArgs]
    options: list[ClickFuncArgs]


def get_config_file_path() -> Path | None:
    # from env var
    env_path = os.getenv("CLIER_CONFIG", None)

    if env_path:
        file_path = Path(env_path)

        if file_path.exists():
            return file_path

    # current dir
    file_path = Path(".clier.yml")
    if file_path.exists():
        return file_path

    # home dir
    file_path = Path("~/.clier.yml").expanduser()
    if file_path.exists():
        return file_path

    return None


def load_command_specs_from_yaml(file_path: Path) -> list[CommandSpec]:
    with open(file_path) as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError("Invalid config file")

    command_specs = []
    for command in config["commands"]:
        arguments = [ClickFuncArgs(**arg) for arg in command["arguments"]]
        options = [ClickFuncArgs(**opt) for opt in command["options"]]
        command_spec = CommandSpec(
            name=command["name"],
            help=command["help"],
            shell=command["shell"],
            arguments=arguments,
            options=options,
        )
        command_specs.append(command_spec)

    return command_specs


@click.group()
@click.version_option()
def cli():
    "Turn shell script into cli command"


@cli.command()
def info():
    """Show the clier config file path to be loaded"""
    file_path = get_config_file_path()
    if not file_path:
        click.echo("No config file found")
        return

    click.echo(file_path.absolute())


def add_command(spec: CommandSpec):
    @cli.command(name=spec.name, help=spec.help)
    def command_func(**kwargs):
        # click.echo(spec.shell)
        # click.echo(kwargs)

        # # use jinja to render the shell script
        template = Template(spec.shell)
        rendered = template.render(kwargs)
        # click.echo(rendered)

        # run the shell script
        for line in run_command(rendered):
            click.echo(line)

    for argument in spec.arguments:
        command_func = click.argument(*argument.arg, **argument.kwargs)(command_func)

    for option in spec.options:
        command_func = click.option(*option.arg, **option.kwargs)(command_func)

    return command_func


def create_and_run_cli():
    # dynamically create commands
    config_file_path = get_config_file_path()
    if not config_file_path:
        click.echo("No config file found")
        sys.exit(1)

    specs = load_command_specs_from_yaml(config_file_path)

    for spec in specs:
        add_command(spec)

    return cli()
