# Continuous Integration

Gitlab has built-in CI tests. These can be configured by editing `.gitlab-ci.yml`. By default, these are run on all pushes and merge requests.

Currently, GitLab is configured to run all Python and JavaScript tests, as well as enforcing the [styleguide](./project-conventions.md#code-styleguide).

## Automatic linting locally

You can also run the linting tests automatically before committing. This is optional. It uses `pre-commit`, which is installed by default in the Vagrant Box, and a `.pre-commit-config.yml` file is included for the project.

To use `pre-commit` when making commits on your host machine you must install `pre-commit`. Either create a virtualenv to use with the project or to install globally.
Please refer to the [`pre-commit` install instructions](https://pre-commit.com/#install) for more information.

`pre-commit` will not run by default. To set it up, run `pre-commit install` inside the Vagrant Box, or on the host if you have installed `pre-commit` there.

If you are using `pre-commit` locally (outside of the Vagrant Box) you will need to install `seed-isort-config` with `pip install seed-isort-config`.

The `detect-secrets` hook requires a baseline secrets file to be included. If you need to, you can update this file, e.g. when adding dummy secrets for unit tests:

```bash
$ detect-secrets scan > .secrets.baseline
```
