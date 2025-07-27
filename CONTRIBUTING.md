# Contributing Guide

This project is intended for personal, non-commercial use. The repository is small and all work happens directly on the `main` branch.

## Code Style
- Use **camelCase** for variables and functions.
- Use **PascalCase** for class names.
- No specific linting tools are enforced yet.
- Module filenames also use camelCase (e.g. `dataHelper.py`).
- Constants are written in **UPPERCASE_WITH_UNDERSCORES**.
- Indent with four spaces.

The `src` directory has a layered structure:
- `main.py` is the entry point and only imports from the *handlers* package.
- Handlers manage user interactions and call functions from the *helpers* package.
- Helpers provide small utilities and work with classes and configuration data.
- Data classes and enums live in the `classes` package.
- Global constants are grouped in `config/constants.py`.
- Translation keys are defined in `classes/textKeys.py` with language files in
  `config/languages`.
- Item and spell data are kept as JSON under the `data/` directory.

## Commit Process
- Commit messages are free-form; structure them as you see fit.
- All contributions are committed to the `main` branch. Feature branches are not required.

## Reporting Bugs and Requesting Features
- When reporting a bug, include a short guide to reproduce the problem.
- For feature requests, describe which files are expected to change.
- Opening an issue prior to a pull request is appreciated but not mandatory.

## Tests and Dependencies
- Automated tests are planned for the future. None exist yet.
- A dependency file is also planned but not yet available.

