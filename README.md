# attercop

[![PyPI version](https://badge.fury.io/py/attercop.svg)](https://badge.fury.io/py/attercop)

Your friendly, micro command line LLM query generation tool

## Overview

attercop is a micro Python tool that generates command prompts via an LLM provider. It uses the OpenAI API to map natural language queries to a command or sequence of commands, emphasizing usage of standard GNU tools. The example I use in the GPT query is:

```bash
$ attercop "List all the files in this directory, filtering out the ones that are not directories, and then sort them by size, largest first."
(1/1) ls -l | grep ^d | sort -k5 -n -r
```

It then lets you cycle through multiple options if the prompt is somewhat ambiguous, and either confirm (and run!) or reject the command.

## Installation

The package is now available on PyPI, so you can install it with pip:

```bash
pip install attercop
```

You will need to set the environment variable `OPENAI_API_KEY` to your personal OpenAI API key. You can get one [here](https://beta.openai.com/).

### What about other LLM providers?

I would definitely prefer this tool to be agnostic to the LLM provider. If you want to add support for another provider, please open an issue or a pull request.

## Usage

Once you've installed, you can just run the `attercop` command:

```bash
$ attercop "Find all files in this and subdirectories ending with the extension .txt"
(1/1): find . -name "*.txt"
```

It will hit the OpenAI API and come back with one of several prompts, depending on the max_prompts parameter. You can cycle through these with tab, select one for execution with enter or 'y', or hit 'q' or Ctrl-C to quit.
