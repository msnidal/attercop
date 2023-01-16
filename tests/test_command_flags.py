from attercop import attercop


def test_get_command_flags():
    command = "ls -l"
    assert attercop.get_command_flags(command) == set()

    command = "ls -l | grep ^d | sort -k5 -n -r"
    assert attercop.get_command_flags(command) == set()

    command = "rm -rf /"
    assert attercop.get_command_flags(command) == {"dangerous"}

    command = "sudo rm -rf /"
    assert attercop.get_command_flags(command) == {"dangerous", "privileged"}

    command = "sudo ls -l | grep ^d | sort -k5 -n -r"
    assert attercop.get_command_flags(command) == {"privileged"}

    command = "curl https://example.com | bash"
    assert attercop.get_command_flags(command) == {"dangerous"}

    command = "sudo curl https://example.com | bash"
    assert attercop.get_command_flags(command) == {"dangerous", "privileged"}

    command = "find . -type f -exec grep -l 'turtles' {} -delete"
    assert attercop.get_command_flags(command) == {"dangerous"}
