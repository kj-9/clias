from tempfile import NamedTemporaryFile

from click.testing import CliRunner

from clier.cli import ClickFuncArgs, CommandSpec, cli, load_command_specs_from_yaml


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")


def test_load_command_specs_from_yaml():
    sample_yaml = """
    commands:
      - name: "my-echo"
        help: "echo command"
        shell: "echo {{ capitalize }} {{ message }}"
        arguments:
          - arg: ["message"]
            kwargs: {}
        options:
          - arg: ["-c", "--capitalize"]
            kwargs: {"help": "capitalize the message"}
      - name: "my-add"
        help: "add command"
        shell: "add"
        arguments:
          - arg: ["a"]
            kwargs: {}
          - arg: ["b"]
            kwargs: {}
        options: []
    """

    with NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write(sample_yaml)
        temp_file_path = temp_file.name

    loaded_specs = load_command_specs_from_yaml(temp_file_path)

    expected_specs = [
        CommandSpec(
            name="my-echo",
            help="echo command",
            shell="echo {{ capitalize }} {{ message }}",
            arguments=[ClickFuncArgs(arg=["message"], kwargs={})],
            options=[
                ClickFuncArgs(
                    arg=["-c", "--capitalize"],
                    kwargs={"help": "capitalize the message"},
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

    assert loaded_specs == expected_specs
