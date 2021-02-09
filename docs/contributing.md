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

1.  View you fork of the repository on GitHub and [create a Pull Request](https://guides.github.com/activities/forking/#making-a-pull-request) back to the `master` branch of the main repository.
    Please include a description of the bug your PR is fixing and why you solved it the way you did.

## How to Handle Contributions

_This section is for maintainers and reviewers of the internal project._

Since CI has not been migrated to GitHub yet, automatic formatting, linting and test are not available at that point. The CI will run once the changes on GitHub are integrated to GitLab.

1.  Review the GitHub Pull Request accoring to the project standards.
1.  Be sure to check for undesired side-effects of the bugfix.
1.  If your happy with the PR, merge it into `master` on GitHub.

`master` on GitHub will be overriden by the next push from GitLab.
To avoid loosing the just merged changes you need to integrate them into the GitLab repo.

1.  Add the GitHub repo to you local development setup.

        git remote add github [Github Repo URL]

1.  Create a new branch from `release` on **GitLab**.

        git checkout release
        git pull origin release
        git checkout -b fix/fix-from-github

1.  Pull fix from `master` on **GitHub** into the new branch

        git pull github master

1.  Push the new branch to **GitLab**.

        git push origin fix/fix-from-github

1.  Check the CI pipline to see if any formatting/linting/tests need to be fixed.
    If so, do this in your local branch and push the changes again.

1.  Create a Merge Request on GitLab for the new branch to the `release` branch.
    Proceed with the normal review and process to make sure we want to include these changes into the project.
