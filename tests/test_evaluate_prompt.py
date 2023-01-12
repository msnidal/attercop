import sys
from unittest.mock import patch, MagicMock

from attercop import attercop


@patch("attercop.attercop.openai.Completion.create")
@patch("attercop.attercop.pyperclip.copy")
@patch("attercop.attercop.subprocess.run")
def test_execute(subprocess_run, pyperclip_copy, openai_completion_create):
    openai_completion_create.return_value = MagicMock(
        choices=[MagicMock(text="echo 'My name jeff'")]
    )

    sys.argv.append("My name jeff")
    sys.argv.append("-X")
    attercop.evaluate_prompt()

    openai_completion_create.assert_called_once()
    subprocess_run.assert_called_once_with("echo 'My name jeff'", shell=True)
    pyperclip_copy.assert_not_called()
