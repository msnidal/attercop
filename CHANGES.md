# Changes

## v0.3.4

* Add `-delete` to the list of dangerous flags, eg. `find . -delete` and similar. Add test as well
* Tweak the dangerous and privileged flag display in interactive mode and use red text with colorama
* Update Python version requirement in README

## v0.3.3

* Improve verbosity behaviour by further specifying prompt and including an additional example

## v0.3.2

* Replace match statement with if/else to support older Python versions back to 3.7.1 (bounded by OpenAI python library)
* Remove newline characters being appended to the end of the command in print mode
* Add tests for print mode branch
* Add changes tracking file for tagged releases
* Add workflow to publish tagged releases to PyPI

## v0.3.1

* Add new print mode to output the command directly to stdout, complete with warnings to stderr for flagged commands
* Improve the README as well as the help prompt

## v0.3.0

* Add direct execution and copy mode to allow for usage in scripts etc. Due to the danger involved here, I added some somewhat stern warnings in the README and help prompts, as well as...
* New `dangerous` and `privileged` flags to try to cover most of the potential pain zones - think sudo rm -rf / and various permutations of deletions and privilege escalations. Will show to the user and refuses to run direct execution mode
* A test suite! Covers most control flow branches, not totally comprehensive yet but I'm verifying execution and copy behaviour in direct and interactive mode, as well as flag parsing as described above
* Github workflow to insist on black linting as well as the passage of the above tests
* Overall misc. improvements to the main execution loop, arguments etc.

## v0.2.0

* Add a verbosity flag `-v | --verbose`, credit to [user chris37879 on reddit for the idea](https://www.reddit.com/r/programming/comments/106q5jh/comment/j3j63nw/?utm_source=reddit&utm_medium=web2x&context=3)! This will encourage the completion to include full verbose flags when available, ie `--help` instead of `-h`.
* Add a shell flag `-s | --shell` and automatic shell detection, to hopefully account for some of the nuance between how ie. bash and zsh or fish handle environment variables, etc.
* Also add an optional API key flag `-K | --api-key` in case people don't want to use the environment variable. Will still default to checking for that env var, and will now throw an exception if nothing is found.
* Fix bug to ensure arguments are actually being used in the API call!
* Fix a potential issue where if duplicate commands are returned in a staggered order, the command cycling may select duplicates instead of the unique values

## v0.1.2

* Documentation and metadata tweaks

## v0.1.1

* Upgrades the default model to `davinci-003` for better performance
* Adds a new copy to clipboard command
* Enhances the README and help text with more details on commands
* Very slight tweak to prompt

## v0.1.0

* Initial release!
