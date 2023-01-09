import os
import argparse
import sys
import tty
import termios
import subprocess
import pathlib

import openai
import pyperclip

ACCEPT, COPY = "y", "c"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a command or chain of shell commands from a natural language prompt. Once generated, you can cycle through commands with tab, accept a command with enter or y, copy to the clipboard with c, or quit with q."
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="The English-language prompt to use for the GPT completion.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prefer verbose flags for the generated command, ie. `--help` instead of `-h`. Defaults to False, though it won't explicitly ask for short flags.",
    )
    parser.add_argument(
        "-n",
        "--num-prompts",
        type=int,
        default=3,
        help="The maximum number of alternative prompts to generate. Defaults to 3.",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=0,
        help="Higher values will result in more diverse completions, but lower values will generally result in more sensible ones. Defaults to 0.",
    )
    parser.add_argument(
        "-m",
        "--max-tokens",
        type=int,
        default=100,
        help="The maximum number of tokens to generate per prompt. Defaults to 100.",
    )
    parser.add_argument(
        "-M",
        "--model",
        type=str,
        default="text-davinci-003",
        help="The GPT model to use. Defaults to text-davinci-003, the latest and most powerful model generally available.",
    )
    parser.add_argument(
        "-K",
        "--api-key",
        type=str,
        default=None,
        help="Manually specify an OpenAI API key to use. If none provided, will default to the OPENAI_API_KEY environment variable.",
    )
    parser.add_argument(
        "-s",
        "--shell",
        type=str,
        default=None,
        help="The shell to use for the generated command, ie. bash, zsh, fish... If none provided, will look for a SHELL environment variable if available, or otherwise default to bash.",
    )
    args = parser.parse_args()

    # Resolve the shell according to the precedence described in the shell argument help
    shell = None
    if args.shell:
        shell = args.shell
    else:
        env_shell = os.getenv("SHELL")
        if env_shell:
            shell = pathlib.Path(env_shell).name # ie. /bin/bash -> bash
        else:
            shell = "bash"

    if args.api_key:
        openai.api_key = args.api_key
    else:
        openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError(
            "No OpenAI API key provided. Please provide an API key either via the -k/--api-key flag, or by setting OPENAI_API_KEY environment variable in your shell."
        )
    
    verbosity_clause = " Use verbose flags wherever possible, ie. --help instead of -h\n" if args.verbose else "\n"
    sort_clause = "sort --key=5 --numeric-sort --reverse\n" if args.verbose else "sort -k5 -n -r\n"
    prompt = (
        f"Convert a prompt into a working programmatic shell command or chain of commands, making use of standard GNU tools and common Unix idioms. The shell used is {shell}."
         + verbosity_clause
         + "Prompt: List all the files in this directory, filtering out the ones that are not directories, and then sort them by size, largest first.\n"
         + "Command: ls -l | grep ^d | "
         + sort_clause
         + f"Prompt: {args.prompt}\n"
         + "Command: "
    )

    return args, prompt


def evaluate_prompt():
    args, prompt = parse_args()

    stdin_descriptor = sys.stdin.fileno()
    stdin_attributes = termios.tcgetattr(stdin_descriptor)
    tty.setraw(stdin_descriptor)

    response = openai.Completion.create(
        model=args.model,
        prompt=prompt,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        top_p=1.0,
        n=args.num_prompts,
        frequency_penalty=0.2,
        presence_penalty=0.0,
        stop=["\n"],
    )

    # Deduplicate choices while still preserving ordering (dict is insertion ordered)
    outputs = list(dict.fromkeys([choice.text for choice in response.choices])) 
    if not "".join(outputs):
        print("No outputs generated. Please try again with a different prompt or model.", end="")
        sys.exit(1)

    action = None
    selected_query = 0

    try:
        while not action:
            output = outputs[selected_query]

            print(f"({selected_query + 1}/{len(outputs)}): {output}", end="\r")
            ch = sys.stdin.read(1)

            match ch:
                case "y" | "\r":
                    action = ACCEPT
                case "c":
                    action = COPY
                case "\t":
                    selected_query = (selected_query + 1) % len(outputs)
                case "q" | "\x03" | "\x04":  # SIGKILL & SIGTERM - not ideal tty handling but hey it works
                    break

            if not action:
                sys.stdout.write("\r" + " " * 100 + "\r")
    finally:
        termios.tcsetattr(stdin_descriptor, termios.TCSADRAIN, stdin_attributes)

    if action == ACCEPT:
        print(f"Executing: {output}")
        subprocess.run(output, shell=True)
    elif action == COPY:
        print(f"Copying to clipboard: {output}")
        pyperclip.copy(output)


if __name__ == "__main__":
    evaluate_prompt()
