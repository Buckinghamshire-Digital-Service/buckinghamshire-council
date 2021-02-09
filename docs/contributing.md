# Contributing

Before contributing to the open source project on GitHub, please consider that this project is opeen source but not collaborative.
The features it includes are specifically designed to the needs of the Buckinghamshire Council.

Feature submissions are unlikely to be included in the project, unless the feature is specifically desired by the council.
Bugfixes will be reviewed and included accoring to the [process described below](#how-to-handle-contributions).
Please be sure to follow the guidelines below on [how to contribute to this open source project](#how-to-contribute-to-the-open-source-project).


## Repository Setup

Internal development happens on an internal GitLab instance.
A merge or push to the protetected `master` branch triggers a push to the open source GitHub repository.

No active development happens on GitHub itself.

The current setup was chosen to allow for open sourcing the repository without the need to migrate the whole CI setup from GitLab to GitHub.
This setup may be changed in the future to remove the need of managing two repositories.

## How to Contribute to the Open Source Project

If you would like to contribute a bugfix to this project, just follow the normal flow for [contributions on GitHub](https://guides.github.com/activities/forking/).

1.  Fork this repository on GitHub to create your own copy of it.
1.  Clone your fork of the repository to your local development machine.

        git clone [URL TO GIT REMOTE]

1.  Create a new branch for the bugfix.

        git checkout -b fix/something-broken

1.  Create a [local setup](/#setting-up-a-local-build) and implement your changes.

        git commit fixed_file.py

1.  Push your local fix branch to your GitHub fork.

        git push origin fix/something-broken

1.  View you fork of the repository on GitHub and [create a Pull Request](https://guides.github.com/activities/forking/#making-a-pull-request) back to the `master` branch of the  main repository.
    Please include a description of the bug your PR is fixing and why you solved it the way you did.

## How to Handle Contributions

_This section is for maintainers and reviewers of the internal project._

