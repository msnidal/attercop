import os
import argparse
import sys
import tty
import termios
import subprocess

import openai
import pyperclip

ACCEPT, COPY = "y", "c"
NUM_PROMPTS = 3
TEMPERATURE = 0
MAX_TOKENS = 100
MODEL = "text-davinci-003"
BASE_PROMPT = """Convert a prompt into a working programmatic bash command or chain of commands, making use of standard GNU tools and common bash idioms.

Prompt: 
List all the files in this directory, filtering out the ones that are not directories, and then sort them by size, largest first.
Command:
ls -l | grep ^d | sort -k5 -n -r

Prompt: 
"""

openai.api_key = os.getenv("OPENAI_API_KEY")
parser = argparse.ArgumentParser(
    description="Generate a command or chain of commands to perform a task. Once generated, you can cycle through commands with tab, accept a command with enter or y, copy to the clipboard with c, or quit with q."
)
parser.add_argument(
    "prompt",
    type=str,
    help="The English-language prompt to use for the GPT completion.",
)
parser.add_argument(
    "--num-prompts",
    type=int,
    default=NUM_PROMPTS,
    help="The maximum number of alternative prompts to generate. Defaults to 3.",
)
parser.add_argument(
    "--temperature",
    type=float,
    default=TEMPERATURE,
    help="Higher values will result in more diverse completions, but lower values will result in more sensible completions. Defaults to 0.",
)
parser.add_argument(
    "--max-tokens",
    type=int,
    default=MAX_TOKENS,
    help="The maximum number of tokens to generate per prompt. Defaults to 100.",
)
parser.add_argument(
    "--model",
    type=str,
    default=MODEL,
    help="The GPT model to use. Defaults to text-davinci-003.",
)

args = parser.parse_args()

stdin_descriptor = sys.stdin.fileno()
stdin_attributes = termios.tcgetattr(stdin_descriptor)
tty.setraw(stdin_descriptor)


def create_prompt():
    user_prompt = BASE_PROMPT + args.prompt + "\nAnswer:\n"

    response = openai.Completion.create(
        model=MODEL,
        prompt=user_prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1.0,
        n=NUM_PROMPTS,
        frequency_penalty=0.2,
        presence_penalty=0.0,
        stop=["\n"],
    )

    outputs = [choice.text for choice in response.choices]
    output_set = set(outputs)

    action = None
    selected_query = 0

    try:
        while not action:
            output = outputs[selected_query]

            print(f"({selected_query + 1}/{len(output_set)}): {output}", end="\r")
            ch = sys.stdin.read(1)

            match ch:
                case "y" | "\r":
                    action = ACCEPT
                case "c":
                    action = COPY
                case "\t":
                    selected_query = (selected_query + 1) % len(output_set)
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
    create_prompt()