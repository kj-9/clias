import click
from dataclasses import dataclass

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
        shell="echo",
        arguments=[
            ClickFuncArgs(
                arg=["message"],
                kwargs={}
            )
        ],
        options=[
            ClickFuncArgs(
                arg=["-c", "--capitalize"],
                kwargs={"help": "capitalize the message"}
            )
        ]
    ),
    CommandSpec(
        name="my-add",
        help="add command",
        shell="add",
        arguments=
        [
            ClickFuncArgs(
                arg=["a"],
                kwargs={}
            ),
            ClickFuncArgs(
                arg=["b"],
                kwargs={}
            )
        ],
        options=[]
    )
]


@click.group()
@click.version_option()
def cli():
    "turn shell script to cli"


# dynamically create commands
for spec in specs:
    @cli.command(name=spec.name, help=spec.help)
    def command_func(**kwargs):
        click.echo(kwargs)

    for argument in spec.arguments:
        command_func = click.argument(*argument.arg, **argument.kwargs)(command_func)

    for option in spec.options:
        command_func = click.option(*option.arg, **option.kwargs)(command_func)

