import pytest

from attercop import attercop


def test_standard_args():
    args = attercop.parse_args(["My name jeff", "-c"])
    assert args.prompt == "My name jeff"
    assert args.copy == True
    assert args.execute == False
    # Defaults
    assert args.model == "text-davinci-003"
    assert args.temperature == 0.0
    assert args.num_prompts == 1  # Copy mode only generates one prompt

    args = attercop.parse_args(
        [
            "Delete the computer",
            "-X",
            "--model",
            "text-davinci-2020-05-03",
            "--temperature",
            "0.5",
        ]
    )
    assert args.prompt == "Delete the computer"
    assert args.execute == True
    assert args.copy == False
    assert args.model == "text-davinci-2020-05-03"
    assert args.temperature == 0.5
    assert args.num_prompts == 1

    args = attercop.parse_args(["Just list some files or something man"])
    assert args.execute == False
    assert args.copy == False
    assert args.num_prompts == 3


def test_arg_errors():
    with pytest.raises(SystemExit):
        attercop.parse_args(["Por que no los dos", "--copy", "--execute"])

    with pytest.raises(SystemExit):
        attercop.parse_args(["Warm it up for me", "--temperature", "80"])

    with pytest.raises(SystemExit):
        attercop.parse_args(
            [
                "I am going to generate ten million tokens and nobody can stop me",
                "--max-tokens",
                "10000000",
            ]
        )

    with pytest.raises(SystemExit):
        attercop.parse_args(["No thoughts head empty", "-n", "0"])
