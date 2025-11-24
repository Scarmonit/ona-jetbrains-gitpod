# Contributing to Ona JetBrains + Gitpod Environment

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/Scarmonit/ona-jetbrains-gitpod/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, versions, etc.)

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or clarify instructions
- Add examples to the custom agents
- Improve README or usage guides
- Add new tutorials or guides

### Adding Examples

To add new example code:

1. Create the example in the appropriate directory (`examples/python`, `examples/nodejs`, or `examples/devops`)
2. Follow the existing code style and patterns
3. Add documentation explaining what the example demonstrates
4. Test the example to ensure it works
5. Update the examples README

### Improving Custom Agents

To improve the Copilot agents:

1. Edit the appropriate agent file in `.github/agents/`
2. Add new patterns, examples, or guidelines
3. Ensure consistency with existing style
4. Test the changes with actual Copilot prompts
5. Document what was changed and why

### Adding New Features

For new features:

1. Open an issue to discuss the feature first
2. Fork the repository
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Make your changes following the style guidelines
5. Test your changes thoroughly
6. Commit with clear, descriptive messages
7. Push to your fork
8. Open a Pull Request

## Development Guidelines

### Code Style

#### Python
- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Use `black` for formatting
- Use `isort` for import sorting

#### JavaScript/TypeScript
- Follow Airbnb style guide
- Use TypeScript when possible
- Use Prettier for formatting
- Use ESLint for linting

#### Shell Scripts
- Use `#!/bin/bash` shebang
- Use `set -euo pipefail`
- Add comments for complex logic

### Git Commit Messages

Follow these guidelines:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests liberally after the first line

Examples:
```
Add PostgreSQL integration example

- Create example with SQLAlchemy
- Add migration scripts
- Update documentation

Fixes #123
```

### Pull Request Process

1. **Update Documentation**: Update README.md and other docs with details of changes
2. **Add Tests**: If applicable, add tests for your changes
3. **Update Examples**: If you change agent behavior, update examples
4. **Update CHANGELOG**: Add your changes to the Unreleased section
5. **Request Review**: Request review from maintainers
6. **Address Feedback**: Respond to and address all review comments
7. **Squash Commits**: Squash commits if requested before merging

### Testing

Before submitting:

1. **Test Examples**: Ensure all example code runs successfully
   ```bash
   # Python examples
   cd examples/python
   python fastapi_example.py
   
   # Node.js examples
   cd examples/nodejs
   npx tsx express_example.ts
   
   # Docker examples
   cd examples/devops
   docker-compose config
   ```

2. **Check Syntax**: Verify syntax of all files
   ```bash
   # Python
   python -m py_compile examples/python/*.py
   
   # YAML
   yamllint .gitpod.yml
   ```

3. **Test Copilot Agents**: Try using the agents with various prompts

4. **Review Documentation**: Ensure all links work and formatting is correct

## Project Structure

```
ona-jetbrains-gitpod/
├── .github/               # GitHub-specific files
│   ├── agents/           # Custom Copilot agent definitions
│   ├── copilot-instructions.md
│   └── COPILOT_USAGE.md
├── .devcontainer/        # Dev container configuration
├── .vscode/              # VS Code settings
├── examples/             # Example code
│   ├── python/          # Python examples
│   ├── nodejs/          # Node.js examples
│   └── devops/          # DevOps examples
├── .gitignore
├── .gitpod.yml
├── CONTRIBUTING.md       # This file
├── README.md
└── IMPLEMENTATION_SUMMARY.md
```

## Custom Agent Guidelines

When editing custom agents in `.github/agents/`:

### Structure
Each agent file should include:
1. **Introduction**: Brief description of the agent's expertise
2. **Expertise Areas**: List of specific capabilities
3. **Code Style**: Language-specific style guidelines
4. **Best Practices**: Patterns and conventions
5. **Examples**: Code snippets demonstrating patterns
6. **Guidelines**: List of key principles
7. **Quick Commands**: Common commands for the domain

### Writing Style
- Be clear and concise
- Provide working code examples
- Include comments explaining key concepts
- Use consistent formatting
- Reference official documentation

### Testing Agents
Test your agent changes by:
1. Using GitHub Copilot Chat with the agent
2. Trying various prompts and scenarios
3. Verifying the suggestions follow the guidelines
4. Checking that examples are accurate

## Code Review Process

All submissions require review. Reviewers will check:

- ✅ Code follows project style guidelines
- ✅ Documentation is clear and accurate
- ✅ Examples work as described
- ✅ Changes are well-tested
- ✅ Commit messages are clear
- ✅ No breaking changes without discussion

## Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and experiences
- Provide constructive feedback
- Celebrate contributions

## Questions?

- Open an issue for questions about contributing
- Tag issues with `question` label
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors will be recognized in:
- README.md (major contributions)
- Git commit history
- GitHub contributors page

Thank you for contributing! 🎉
