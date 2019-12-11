# Buckinghamshire Council — Continuous Integration

Gitlab has built-in CI tests. These can be configured by editing `.gitlab-ci.yml`. By default, these are run on all pushes and merge requests.

## Code styleguide

This project’s code formatting is enforced with [Prettier](https://prettier.io/) for supported languages. Make sure to have Prettier integrated with your editor to auto-format when saving files, or to manually run it before committing (`npm run format`).

## Automatic linting locally

You can also run the linting tests automatically before committing. This is optional. It uses pre-commit, which is installed by default in the vagrant box, and a .pre-commit-config.yml file is included for the project.

To use when making commits on your host machine you must install pre-commit, either create a virtualenv to use with the project or to install globally see instructions at (https://pre-commit.com/#install).

Pre-commit will not run by default. To set it up, run `pre-commit install` inside the Vagrant box, or on the host if you have installed pre-commit there.

If you are using pre-commit locally (outside of vagrant) you will need to install seed-isort-config with `pip install seed-isort-config`.

    The `detect-secrets` hook requires a baseline secrets file to be included. If you need to, you can update this file, e.g. when adding dummy secrets for unit tests:

    ```bash
    $ detect-secrets scan > .secrets.baseline
    ```
