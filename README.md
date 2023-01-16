# attercop

[![PyPI](https://img.shields.io/pypi/v/attercop?color=gr)](https://pypi.org/project/attercop/#description)
![PyPI - Python Version](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fattercop%2Fjson)
![PyPI - License](https://img.shields.io/pypi/l/attercop)
![Code Style - Black](https://img.shields.io/badge/code%20style-black-black)

Your friendly natural language shell command generation tool!

## Overview

Attercop is a micro command line tool that generates shell commands from natural language, by way of an external large language model. Written in Python, it uses the OpenAI API to map a descriptive English language query to a command or sequence of commands, emphasizing usage of standard coreutils and tailored to the user's shell - it does its best to support bash, fish, zsh and more. For example:

```bash
$ attercop "List all the files in this directory, filtering out the ones that are not directories, and then sort them by size, largest first."
(1/1) ls -l | grep ^d | sort -k5 -n -r
```

In its default interactive mode, attercop will let you cycle through multiple options with `Tab` if the prompt is somewhat ambiguous, and either confirm and execute the output with `y` or `Enter`, copy it to the clipboard with `c`, or outright reject the command with `q`, `Ctrl+C` or `Ctrl+D`. Attercop also provides direct execution, copy and print modes to support a variety of workflows, as well as a number of optional parameters to tweak the command generation, such as the verbosity of command flags with `-v`, temperature with `-t` (essentially how creative it will get) and the max command output length `-m` as measured in GPT tokens.

## Installation

Attercop is available on PyPI, so as long as you're running Python >=3.7.1, you can install it with pip:

```bash
pip install attercop
```

You will need to set the environment variable `OPENAI_API_KEY` to your personal OpenAI API key. [You can get one here](https://beta.openai.com/) - as of January 2023, as a new member you will get plenty of free credits to play with. [For more on pricing you can see their page here.](https://openai.com/api/pricing/). Optionally you may also pass the API key as a command line argument with the `-K` or `--api-key` flag.

For developers, you can also install from source by running `pip install -e .[lint,test]` in the root directory after cloning the repository. Tests can be run locally with `pytest` and linting with `black` if you include both optional dependencies.

## Usage

Once you've installed the tool, you can just run the `attercop` command:

```bash
$ attercop "Find all files in this and subdirectories ending with the extension .txt"
(1/1): find . -name "*.txt"
```

It will hit the OpenAI API and come back with one of several prompts, depending on the max_prompts parameter.

### Interactive Mode

By default, attercop will run in interactive mode, in which the user will be prompted for confirmation before any command is executed or copies. The interactive mode controls are as follows:

| Command           | Key                         |
|-------------------|-----------------------------|
| Cycle Command     | `Tab`                       |
| Execute           | `y` \| `Enter`              |
| Copy to Clipboard | `c`                         |
| Reject            | `q` \| `Ctrl+C` \| `Ctrl+D` |

### Execute Mode

Optionally, you can also include the `-X` or `--execute` flag to execute the command **immediately without confirmation**. Please approach with great caution! Although direct execution mode may be useful for certain workflows, it should nonetheless be approached carefully as you are asking attercop to execute arbitrary commands on your system **without any confirmation!** attercop does its best to identify dangerous (removing files, curling inputs for execution, etc.) or privileged (sudo, su...) commands and will exit direct execution mode if identified as such, but it is important to note that this is not a guarantee of safety and it should nonetheless be used with great caution and care. If you are unsure, it is always recommended to use the default interactive mode.

### Copy Mode

Direct copy mode with the `-c` or `--copy` flag similarly copies the output directly to your clipboard without confirmation. This is more lenient and will not exit if a dangerous command is identified, though it will print a warning to the console (via stderr) - please use caution and review the command before executing!

### Print Mode

Print mode with the `-p` or `--print` flag outputs the generated command directly to stdout without prompting for user input. Similarly to copy mode, will not exit if a dangerous command is executed, but will print a warning to stderr.

## Help and Options

For the full menu of options and optional arguments, including various parameters to tweak the API call, see `attercop --help`:

```
$ attercop --help
usage: attercop [-h] [-X | -c | -p] [-v] [-n [1, 10]] [-t [0, 2]] [-m [1, 1024]] [-M MODEL] [-K API_KEY] [-s SHELL] prompt

Generate a command or chain of shell commands from a natural language prompt. In the default interactive mode, you can cycle through commands with tab, execute with enter or y, copy to the clipboard with c, or quit with q.

positional arguments:
  prompt                The English-language prompt to use for the GPT completion.

options:
  -h, --help            show this help message and exit
  -X, --execute         Execute mode: runs the generated command immediately without confirmation! Tries to identify dangerous or privileged commands and exit, but should nonetheless be used with great caution.
  -c, --copy            Copy mode: copies the generated command to the clipboard immediately without prompting for user input.
  -p, --print           Print mode: outputs the generated command directly to stdout without prompting for user input.
  -v, --verbose         Explicitly prefer verbose flags for the generated command, ie. `--help` instead of `-h`.
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

## FAQ

### What is a token and how do I know how many I need?

Tokens are the basic unit of text in the GPT-3 API. They represent a sort of piece of a word or, in our case, a kind of "stem" of a command. [You can read more about the concept here](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them) - the default max tokens is 100, which is generally enough to generate all but the most complex of chained commands. If you are doing something super crazy, you may need to increase this value - you can use the `-m` or `--max-tokens` flag to set this value manually.

### What about support for other LLM providers?

I would definitely prefer this tool to be agnostic to the LLM provider. Right now OpenAI is pretty much the only game in town but if you have an idea to add support for another provider (including perhaps a locally-hosted GPT variant) please open an issue or a pull request! Also please do open an issue if you have any other suggestions, identify any bugs or have any feedback more broadly.

### Why GPLv3 and not MIT?

A strange bearded man came to me in a dream and told me to do so before launching into a diatribe about the immorality of buying parrots. Not sure what that last part was all about but hey, I'm not one to tempt fate.

### Why is this tool called attercop?

Mainly I just thought it sounded cool! If you really must know, its from an old English word for spider, and [referenced in a song Bilbo sings in The Hobbit to lure away some spiders from his friends who are stuck in a tree.](https://tolkiengateway.net/wiki/Old_fat_spider_spinning_in_a_tree!) So the connection with the tool is quite tenuous but I suppose you could draw some kind of analogy to the web of manpages that one must traverse to find the right flags for a command, ha ha.
