import sys
from unittest.mock import patch, MagicMock

import pytest

from attercop import attercop

PROMPT = "My name jeff"
COMPLETION = "echo 'My name jeff'"
ALT_COMPLETION = f"{COMPLETION} | grep 'My name jeff'"
DANGER_COMPLETION = "grep -rl 'turtles' | xargs rm"


@pytest.fixture()
def mock_interfaces(mocker):
    """Mocks interfaces to OpenAI and both output modes"""
    openai_completion_create = mocker.patch(
        "attercop.attercop.openai.Completion.create"
    )
    pyperclip_copy = mocker.patch("attercop.attercop.pyperclip.copy")
    subprocess_run = mocker.patch("attercop.attercop.subprocess.run")

    return openai_completion_create, pyperclip_copy, subprocess_run


@pytest.fixture()
def mock_interactive_tty(mocker):
    """Mocks interactive TTY interfaces"""
    stdin_descriptor = mocker.patch("attercop.attercop.sys.stdin.fileno")
    stdin_attributes = mocker.patch("attercop.attercop.termios.tcgetattr")
    tty_setraw = mocker.patch("attercop.attercop.tty.setraw")
    tty_tcsetattr = mocker.patch("attercop.attercop.termios.tcsetattr")
    sys_read = mocker.patch("attercop.attercop.sys.stdin.read")

    return (stdin_descriptor, stdin_attributes, tty_setraw, tty_tcsetattr, sys_read)


def test_direct_execution(mock_interfaces):
    """Tests nominal execution of a single completion in direct mode"""
    openai_completion_create, pyperclip_copy, subprocess_run = mock_interfaces

    openai_completion_create.return_value = MagicMock(
        choices=[MagicMock(text=COMPLETION)]
    )

    sys.argv = [sys.argv[0], PROMPT, "-X"]
    attercop.evaluate_prompt()

    openai_completion_create.assert_called_once()
    subprocess_run.assert_called_once_with(COMPLETION, shell=True)
    pyperclip_copy.assert_not_called()


def test_dangerous_direct_execution(mock_interfaces):
    """Test abort of dangerous execution in direct mode"""
    openai_completion_create, pyperclip_copy, subprocess_run = mock_interfaces

    openai_completion_create.return_value = MagicMock(
        choices=[MagicMock(text=DANGER_COMPLETION)]
    )

    sys.argv = [sys.argv[0], PROMPT, "-X"]

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        attercop.evaluate_prompt()

    openai_completion_create.assert_called_once()
    subprocess_run.assert_not_called()
    pyperclip_copy.assert_not_called()


def test_direct_copy(mock_interfaces):
    """Tests nominal copy of a single completion in direct mode"""
    openai_completion_create, pyperclip_copy, subprocess_run = mock_interfaces

    openai_completion_create.return_value = MagicMock(
        choices=[MagicMock(text=COMPLETION)]
    )

    sys.argv = [sys.argv[0], PROMPT, "-c"]
    attercop.evaluate_prompt()

    openai_completion_create.assert_called_once()
    subprocess_run.assert_not_called()
    pyperclip_copy.assert_called_once_with(COMPLETION)


def test_interactive_execution(mock_interfaces, mock_interactive_tty):
    """Tests nominal execution of a completion in interactive mode

    This test mocks the TTY interfaces and simulates a user cycling around
    before accepting an alternative completion for execution.
    """
    openai_completion_create, pyperclip_copy, subprocess_run = mock_interfaces
    (
        stdin_descriptor,
        stdin_attributes,
        tty_setraw,
        tty_tcsetattr,
        sys_read,
    ) = mock_interactive_tty

    openai_completion_create.return_value = MagicMock(
        choices=[MagicMock(text=COMPLETION), MagicMock(text=ALT_COMPLETION)]
    )

    sys.argv = [sys.argv[0], PROMPT]
    sys_read.side_effect = ["\t"] * 3 + ["y"]

    attercop.evaluate_prompt()

    openai_completion_create.assert_called_once()
    subprocess_run.assert_called_once_with(ALT_COMPLETION, shell=True)
    pyperclip_copy.assert_not_called()

    stdin_descriptor.assert_called_once()
    stdin_attributes.assert_called_once()
    tty_setraw.assert_called_once()
    tty_tcsetattr.assert_called_once()

    assert sys_read.call_count == 4


def test_interactive_reject(mock_interfaces, mock_interactive_tty):
    """Tests nominal rejection of a completion in interactive mode"""
    openai_completion_create, pyperclip_copy, subprocess_run = mock_interfaces
    (
        stdin_descriptor,
        stdin_attributes,
        tty_setraw,
        tty_tcsetattr,
        sys_read,
    ) = mock_interactive_tty

    openai_completion_create.return_value = MagicMock(
        choices=[MagicMock(text=COMPLETION)]
    )

    sys.argv = [sys.argv[0], PROMPT]
    sys_read.side_effect = ["\t", "q"]

    attercop.evaluate_prompt()

    openai_completion_create.assert_called_once()
    subprocess_run.assert_not_called()
    pyperclip_copy.assert_not_called()

    stdin_descriptor.assert_called_once()
    stdin_attributes.assert_called_once()
    tty_setraw.assert_called_once()
    tty_tcsetattr.assert_called_once()

    assert sys_read.call_count == 2
