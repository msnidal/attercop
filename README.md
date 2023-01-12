# attercop

[![PyPI](https://img.shields.io/pypi/v/attercop?color=gr)](https://pypi.org/project/attercop/#description)
![PyPI - Python Version](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fattercop%2Fjson)
![PyPI - License](https://img.shields.io/pypi/l/attercop)
![Code Style - Black](https://img.shields.io/badge/code%20style-black-black)

Your friendly, micro command line LLM query generation tool!

## Overview

attercop is a micro Python tool that generates command prompts via an LLM provider. It uses the OpenAI API to map natural language queries to a command or sequence of commands, emphasizing usage of standard GNU tools. The example I use in the GPT query is:

```bash
$ attercop "List all the files in this directory, filtering out the ones that are not directories, and then sort them by size, largest first."
(1/1) ls -l | grep ^d | sort -k5 -n -r
```

It then lets you cycle through multiple options with `Tab` if the prompt is somewhat ambiguous, and either confirm and run with `y` or `Enter`, copy to clipboard with `c`, or outright reject the command with `q`, `Ctrl+C` or `Ctrl+D`.

## Installation

The package is now available on PyPI, so as long as you're running Python >=3.10, you can install it with pip:

```bash
pip install attercop
```

You will need to set the environment variable `OPENAI_API_KEY` to your personal OpenAI API key. [You can get one here](https://beta.openai.com/) - as of January 2023, as a new member you will get plenty of free credits to play with. [For more on pricing you can see their page here.](https://openai.com/api/pricing/)

## Usage

Once you've installed, you can just run the `attercop` command:

```bash
$ attercop "Find all files in this and subdirectories ending with the extension .txt"
(1/1): find . -name "*.txt"
```

It will hit the OpenAI API and come back with one of several prompts, depending on the max_prompts parameter. The commands in interactive mode are specified below:

| Command           | Key                         |
|-------------------|-----------------------------|
| Cycle Command     | `Tab`                       |
| Execute           | `y` \| `Enter`              |
| Copy to Clipboard | `c`                         |
| Reject            | `q` \| `Ctrl+C` \| `Ctrl+D` |

### Direct Execution and Copy Mode

Optionally, you can also include the `-X` or `--execute` flag to execute the command **immediately without confirmation**. Please approach with great caution! Although direct execution mode may be useful for certain workflows, it should nonetheless be approached carefully as you are asking attercop to execute arbitrary commands on your system **without any confirmation!** Attercop does its best to identify dangerous (removing files, curling inputs for execution, etc.) or privileged (sudo, su...) commands and will exit direct execution mode if identified as such, but it is important to note that this is not a guarantee of safety and it should nonetheless be used with great caution and care. If you are unsure, it is always recommended to use the default interactive mode.

Direct copy mode with the `-c` or `--copy` flag similarly copies the output directly to your clipboard without confirmation. This is more lenient and will not exit if a dangerous command is identified, though it will print a warning to the console - please be careful when executing these commands!

### Full Options

For the full list of options, see `attercop --help`:

```
$ attercop --help
usage: attercop [-h] [-v] [-X] [-c] [-n [1, 10]] [-t [0, 2]] [-m [1, 1024]] [-M MODEL] [-K API_KEY] [-s SHELL] prompt

Generate a command or chain of shell commands from a natural language prompt. Once generated, you can cycle through commands with tab, accept a command with enter or y, copy to the clipboard with c, or quit with q.

positional arguments:
  prompt                The English-language prompt to use for the GPT completion.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Explicitly prefer verbose flags for the generated command, ie. `--help` instead of `-h`.
  -X, --execute         Execute the generated command immediately *without confirmation!* Attercop will do its best to identify dangerous or privileged commands and exit, but should nonetheless be used with great caution. Mutually exclusive with -c | --copy.
  -c, --copy            Copy the generated command to the clipboard immediately, rather than prompting for user input. Mutually exclusive with -X | --execute.
  -n [1, 10], --num-prompts [1, 10]
                        The maximum number of alternative prompts to generate. Defaults to 3.
  -t [0, 2], --temperature [0, 2]
                        Higher values will result in more diverse completions, but lower values will generally result in more sensible ones. Defaults to 0.
  -m [1, 1024], --max-tokens [1, 1024]
                        The maximum number of tokens to generate per prompt. Defaults to 100.
  -M MODEL, --model MODEL
                        The GPT model to use. Defaults to text-davinci-003, the latest and most powerful model generally available.
  -K API_KEY, --api-key API_KEY
                        Manually specify an OpenAI API key to use. If none provided, will default to the OPENAI_API_KEY environment variable.
  -s SHELL, --shell SHELL
                        The shell to use for the generated command, ie. bash, zsh, fish, etc. If none provided, will look for a SHELL environment variable if available, or otherwise default to bash.
```

## What about other LLM providers?

I would definitely prefer this tool to be agnostic to the LLM provider. If you want to add support for another provider, please open an issue or a pull request! Also feel free to open an issue if you have any other suggestions or feedback.
