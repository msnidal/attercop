# attercop

Command line LLM query generation tool

## Overview

attercop is a command line tool for generating LLM queries. It uses the OpenAI API to map natural language queries to a command or sequence of commands, emphasizing usage of standard GNU tools.

## Installation

The package is available on PyPI, so you can install it with pip:

```bash
pip install attercop
```

You will need to set the environment variable `OPENAI_API_KEY` to your personal OpenAI API key. You can get one [here](https://beta.openai.com/).

### What about other LLM providers?

I would definitely prefer this tool to be agnostic to the LLM provider. If you want to add support for another provider, please open an issue or a pull request.

## Usage

Once you've installed, you can just run the `attercop` command:

```bash
attercop "I want to know if the user is logged in"
```

It will hit the OpenAI API and come back with one of several prompts, depending on the max_prompts parameter. You can cycle through these with tab, select one with enter or 'y', or hit 'q' or Ctrl-C to quit.
