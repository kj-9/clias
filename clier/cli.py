import os
import sys
from dataclasses import dataclass
from pathlib import Path

import click
import yaml  # type: ignore
from jinja2 import Template

from clier.run import run_command


@dataclass
class OptionSpec:
    name: list[str]
    help: str


@dataclass
class ArgumentSpec:
    name: str


@dataclass
class CommandSpec:
    name: str
    help: str
    arguments: list[ArgumentSpec]
    options: list[OptionSpec]
    command: str


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
        arguments = [ArgumentSpec(**arg) for arg in command.get("arguments", [])]
        options = [OptionSpec(**opt) for opt in command.get("options", [])]
        command_spec = CommandSpec(
            name=command["name"],
            help=command["help"],
            command=command["command"],
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


def add_command(cli, spec: CommandSpec):
    @cli.command(name=spec.name, help=spec.help)
    def command_func(**kwargs):
        template = Template(spec.command)
        rendered = template.render(kwargs)
        # click.echo(rendered)

        # run the shell script
        for line in run_command(rendered):
            click.echo(line)

    for argument in spec.arguments:
        command_func = click.argument(argument.name)(command_func)

    for option in spec.options:
        kwargs = option.__dict__
        name = kwargs.pop("name")
        command_func = click.option(*name, **kwargs)(command_func)

    return command_func


# dynamically create commands
config_file_path = get_config_file_path()
if not config_file_path:
    click.echo("No config file found")
    sys.exit(1)

specs = load_command_specs_from_yaml(config_file_path)

for spec in specs:
    add_command(cli, spec)
