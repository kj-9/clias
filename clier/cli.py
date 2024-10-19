from dataclasses import dataclass

import click
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


specs: list[CommandSpec] = [
    CommandSpec(
        name="my-echo",
        help="echo command",
        shell="echo {{ capitalize }} {{ message }}",
        arguments=[ClickFuncArgs(arg=["message"], kwargs={})],
        options=[
            ClickFuncArgs(
                arg=["-c", "--capitalize"], kwargs={"help": "capitalize the message"}
            )
        ],
    ),
    CommandSpec(
        name="my-add",
        help="add command",
        shell="add",
        arguments=[
            ClickFuncArgs(arg=["a"], kwargs={}),
            ClickFuncArgs(arg=["b"], kwargs={}),
        ],
        options=[],
    ),
]


@click.group()
@click.version_option()
def cli():
    "turn shell script to cli"


def create_command(spec: CommandSpec):
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


# dynamically create commands
for spec in specs:
    create_command(spec)
