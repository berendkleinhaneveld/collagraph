# Pull Request Process

This guide explains how to submit pull requests to Collagraph and what to expect during the review process.

## Before You Start

1. **Check existing issues** - Look for related issues or discussions
2. **Discuss major changes** - For significant features, open an issue first to discuss the approach
3. **Read the documentation** - Familiarize yourself with the codebase and architecture
4. **Set up your environment** - Follow the [Development Setup](setup.md) guide

## Forking the Repository

1. Fork the repository on GitHub by clicking the "Fork" button
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/collagraph.git
cd collagraph
```

3. Add the upstream repository as a remote:

```bash
git remote add upstream https://github.com/fork-tongue/collagraph.git
```

4. Verify your remotes:

```bash
git remote -v
# origin    https://github.com/YOUR_USERNAME/collagraph.git (fetch)
# origin    https://github.com/YOUR_USERNAME/collagraph.git (push)
# upstream  https://github.com/fork-tongue/collagraph.git (fetch)
# upstream  https://github.com/fork-tongue/collagraph.git (push)
```

## Creating a Feature Branch

Always create a new branch for your work:

```bash
# Update master branch
git checkout master
git pull upstream master

# Create a new feature branch
git checkout -b feature/my-feature-name

# Or for bug fixes
git checkout -b fix/issue-123-description
```

### Branch Naming Conventions

- `feature/description` - For new features
- `fix/description` - For bug fixes
- `docs/description` - For documentation updates
- `refactor/description` - For code refactoring
- `test/description` - For test additions/improvements

Examples:
- `feature/add-computed-properties`
- `fix/issue-45-memory-leak`
- `docs/update-renderer-guide`

## Making Changes

### Development Workflow

1. Install dependencies and pre-commit hooks:

```bash
uv sync --all-groups
uv run pre-commit install
```

2. Make your changes following the [Code Style Guide](code-style.md)

3. Add tests for your changes (see [Testing Guidelines](testing.md))

4. Run tests locally:

```bash
uv run pytest
```

5. Check code quality:

```bash
uv run ruff check .
uv run ruff format .
```

### Commit Your Changes

Stage and commit your changes:

```bash
git add .
git commit -m "Your commit message"
```

Pre-commit hooks will automatically run:
- Linting with ruff
- Formatting check with ruff
- Test suite with pytest

If hooks fail, fix the issues and try again.

## Writing Good Commit Messages

### Format

Follow the conventional commit format:

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

#### Simple commit:

```
fix: prevent memory leak in fragment cleanup

The fragment cleanup was not properly removing event listeners,
causing memory leaks in long-running applications.
```

#### Commit with issue reference:

```
feat: add support for async lifecycle hooks

Closes #123
```

#### Breaking change:

```
feat!: change renderer interface for better performance

BREAKING CHANGE: The create_element method now requires a parent
parameter. Existing custom renderers will need to be updated.
```

### Best Practices

- Use the imperative mood ("add feature" not "added feature")
- Keep the subject line under 50 characters
- Separate subject from body with a blank line
- Wrap the body at 72 characters
- Explain what and why, not how
- Reference issues and PRs when relevant

## Creating a Pull Request

### Push Your Branch

```bash
git push origin feature/my-feature-name
```

### Open the PR

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Select the base repository: `fork-tongue/collagraph`
4. Select the base branch: `master`
5. Fill out the PR template (see below)

### PR Description Guidelines

A good PR description should include:

#### Title

- Clear and concise
- Follows the same conventions as commit messages
- Example: `feat: add template ref support`

#### Description Template

```markdown
## Description

Brief description of what this PR does and why.

## Changes

- Bullet point list of changes
- Keep it high-level
- Focus on what changed, not implementation details

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

Describe how you tested your changes:
- What tests did you add?
- What manual testing did you do?
- What edge cases did you consider?

## Checklist

- [ ] My code follows the project's code style
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Related Issues

Closes #123
Related to #456
```

### Example PR Description

```markdown
## Description

Adds support for template refs, allowing components to get direct references
to DOM elements and child components.

## Changes

- Added `refs` reactive property to Component class
- Implemented `ref` attribute handling in Fragment
- Added tests for static and dynamic refs
- Updated documentation with template refs guide

## Type of Change

- [x] New feature (non-breaking change which adds functionality)

## Testing

- Added comprehensive test suite in `tests/test_template_refs.py`
- Tested with both PySide and Dict renderers
- Verified dynamic ref updates work correctly
- Tested ref cleanup on component unmount

## Checklist

- [x] My code follows the project's code style
- [x] I have performed a self-review of my own code
- [x] I have added tests that prove my feature works
- [x] New and existing unit tests pass locally with my changes
- [x] I have updated the documentation

## Related Issues

Closes #140
```

## CI/CD Checks

When you open a PR, automated checks will run:

### Lint Check

Runs `ruff check` and `ruff format --check` to ensure code style:

```yaml
- name: Lint
  run: uv run --no-sync ruff check .
- name: Format
  run: uv run --no-sync ruff format --check .
```

### Test Suite

Runs tests on multiple Python versions (3.10-3.14):

```yaml
- name: Test
  run: uv run pytest -v --cov=collagraph --cov-report=term-missing
```

### Build Check

Verifies the package builds correctly:

```yaml
- name: Build wheel
  run: uv build
- name: Twine check
  run: uv run twine check dist/*
```

### Fixing CI Failures

If CI checks fail:

1. **Lint failures**: Run `uv run ruff check --fix .` and `uv run ruff format .`
2. **Test failures**: Run `uv run pytest -v` locally to reproduce and fix
3. **Build failures**: Ensure `pyproject.toml` is valid and dependencies are correct

Push fixes to the same branch:

```bash
git add .
git commit -m "fix: address CI feedback"
git push origin feature/my-feature-name
```

The PR will automatically update and re-run checks.

## Code Review Process

### What to Expect

1. **Initial review** - A maintainer will review within a few days
2. **Feedback** - You may receive questions or change requests
3. **Discussion** - Feel free to discuss and ask questions
4. **Iterations** - Make requested changes and push updates
5. **Approval** - Once approved, a maintainer will merge

### Responding to Feedback

When you receive review comments:

1. **Read carefully** - Understand the feedback before responding
2. **Ask questions** - If unclear, ask for clarification
3. **Make changes** - Address the feedback in new commits
4. **Respond** - Comment when you've addressed each point
5. **Request re-review** - Click "Re-request review" when ready

### Making Updates

```bash
# Make the requested changes
# ... edit files ...

# Commit the changes
git add .
git commit -m "refactor: address review feedback"

# Push to the same branch
git push origin feature/my-feature-name
```

### Keeping Your PR Updated

If the master branch has moved ahead:

```bash
# Update your local master
git checkout master
git pull upstream master

# Rebase your feature branch
git checkout feature/my-feature-name
git rebase master

# Force push (be careful!)
git push origin feature/my-feature-name --force-with-lease
```

## Merging Process

### Requirements for Merge

- [ ] All CI checks passing
- [ ] At least one approval from a maintainer
- [ ] No unresolved review comments
- [ ] Up to date with master branch
- [ ] No merge conflicts

### Merge Methods

The maintainer will choose the appropriate method:

- **Squash and merge** - For feature branches with many commits
- **Rebase and merge** - For clean commit history
- **Merge commit** - For branches with meaningful commit history

Most PRs use **squash and merge** for a clean history.

## After Your PR is Merged

1. **Delete your branch** (GitHub will prompt you)
2. **Update your local repository**:

```bash
git checkout master
git pull upstream master
git branch -d feature/my-feature-name  # Delete local branch
```

3. **Celebrate!** You've contributed to Collagraph!

## Common Issues

### Merge Conflicts

If you have merge conflicts:

```bash
# Update master and rebase
git checkout master
git pull upstream master
git checkout feature/my-feature-name
git rebase master

# Resolve conflicts in your editor
# ... fix conflicts ...

git add .
git rebase --continue
git push origin feature/my-feature-name --force-with-lease
```

### Pre-commit Hooks Failing

If hooks fail locally:

```bash
# Fix linting issues
uv run ruff check --fix .

# Fix formatting
uv run ruff format .

# Run tests
uv run pytest

# Try committing again
git commit -m "your message"
```

### Tests Passing Locally but Failing in CI

This can happen due to:
- Different Python versions
- Missing dependencies
- Environment differences

Check the CI logs carefully and try to reproduce with the same Python version.

## Getting Help

- **Questions about your PR**: Comment on the PR
- **General questions**: Open a discussion on GitHub
- **Bug reports**: Open an issue
- **Real-time help**: Check if there's a Discord/Slack (if available)

## Best Practices

### DO

- Keep PRs focused and small
- Write clear descriptions
- Add tests for new features
- Update documentation
- Respond to feedback promptly
- Be patient and respectful

### DON'T

- Submit PRs with failing tests
- Make unrelated changes in the same PR
- Force push after review has started (unless necessary)
- Ignore review feedback
- Submit duplicate PRs
- Take review feedback personally

## Recognition

All contributors are valued! Your contributions will be:
- Acknowledged in the commit history
- Potentially mentioned in release notes
- Appreciated by the community

Thank you for contributing to Collagraph!

## See Also

- [Development Setup](setup.md)
- [Code Style Guide](code-style.md)
