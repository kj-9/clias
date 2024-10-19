# clier

[![PyPI](https://img.shields.io/pypi/v/clier.svg)](https://pypi.org/project/clier/)
[![Changelog](https://img.shields.io/github/v/release/kj-9/clier?include_prereleases&label=changelog)](https://github.com/kj-9/clier/releases)
[![Tests](https://github.com/kj-9/clier/actions/workflows/ci.yml/badge.svg)](https://github.com/kj-9/clier/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/kj-9/clier/blob/master/LICENSE)

Turn shell script into cli command

## Installation

Install this tool using `pip`:
```bash
pip install clier
```
## Usage

For help, run:
<!-- [[[cog
import cog
from clier import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: clier")
cog.out(
    f"```bash\n{help}\n```"
)
]]] -->
```bash
Usage: clier [OPTIONS] COMMAND [ARGS]...

  Turn shell script into cli command

Options:
  -d, --dryrun  dry run mode, only show the rendered command
  --version     Show the version and exit.
  --help        Show this message and exit.

Commands:
  info  Show the clier config file path to be loaded

```
<!-- [[[end]]] -->

You can also use:
```bash
python -m clier --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd clier
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
make install-e
```
To run the tests:
```bash
make test
```

To run pre-commit to lint and format:
```bash
make check
```

`make check` detects if cli help message in `README.md` is outdated and updates it.

To update cli help message `README.md`:
```bash
make readme
```

this runs [cog](https://cog.readthedocs.io/en/latest/) on README.md and updates the help message inside it.
