# Contributing to Nexus MCP

First off, thank you for considering contributing to Nexus MCP! It's people like you that make Nexus MCP such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots and animated GIFs if possible
* Include your environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful
* List some other tools or applications where this enhancement exists

### Pull Requests

* Fork the repo and create your branch from `main`
* If you've added code that should be tested, add tests
* If you've changed APIs, update the documentation
* Ensure the test suite passes
* Make sure your code lints
* Issue that pull request!

## Development Process

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Write or adapt tests as needed
5. Update documentation as needed
6. Submit a pull request

### Development Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

3. Create a branch:
```bash
git checkout -b feature/your-feature-name
```

### Coding Style

* Follow PEP 8 guidelines
* Use type hints
* Write docstrings for all public methods
* Keep functions focused and small
* Use meaningful variable names
* Comment complex logic

### Testing

* Write unit tests for new features
* Ensure all tests pass before submitting PR
* Maintain test coverage above 80%
* Use pytest for testing

### Documentation

* Update README.md if needed
* Add docstrings to new functions
* Update API documentation
* Include examples for new features

## Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🎨 `:art:` when improving the format/structure of the code
    * 🐎 `:racehorse:` when improving performance
    * 🚱 `:non-potable_water:` when plugging memory leaks
    * 📝 `:memo:` when writing docs
    * 🐛 `:bug:` when fixing a bug
    * 🔥 `:fire:` when removing code or files
    * 💚 `:green_heart:` when fixing the CI build
    * ✅ `:white_check_mark:` when adding tests
    * 🔒 `:lock:` when dealing with security
    * ⬆️ `:arrow_up:` when upgrading dependencies
    * ⬇️ `:arrow_down:` when downgrading dependencies

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

* `bug` - Issues that are bugs
* `documentation` - Issues for improving or updating our documentation
* `enhancement` - Issues for new features or improvements
* `help wanted` - Issues where we need assistance from the community
* `question` - Issues that are questions or need discussion
* `security` - Issues that have security implications
* `technical-debt` - Issues related to technical debt or refactoring
* `tests` - Issues related to tests or test coverage

## Recognition

Contributors who submit a PR that is merged will be added to our Contributors list in the README.

## Questions?

Feel free to contact us if you have any questions. You can reach us at:

* Email: contributors@nexusmcp.net
* Twitter: [@NexusMCP](https://twitter.com/NexusMCP) 