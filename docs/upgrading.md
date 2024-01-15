# Upgrading guidelines

This document describes aspects of the system which should be given particular attention when upgrading Wagtail or its dependencies.

## Wagtail package dependencies

We are maintaining our own forks of Wagtail packages at: <https://github.com/torchbox-forks>.

The enables any team member to propose a change to a package, we can all work directly on the work branch and submit it to the original author for consideration.

- [How we work on forked packages (intranet article).](https://intranet.torchbox.com/torchbox-teams/tech-team/working-with-3rd-party-packages/#forking-repositories)
- [Where we manage forked packages (Monday board).](https://torchbox.monday.com/boards/1124794299)

As much as possible, we want to use the official releases available on PyPI for the Wagtail package dependencies. A temporary solution is to fork the package dependency, tag the working branch, and use the tag in the pyproject file.

### Check these packages for updates

**Last tested for wagtail 5.2 upgrade** Comments in the pyproject.toml file may have more detailed information.

- wagtail-django-recaptcha

It is important to replace the usage of the git tags in the pyproject.toml file with the official release version from PyPI as soon as they become available.

## Critical paths

The following areas of functionality are critical paths for the site which don't have full automated tests and should be checked manually.

(If this information is managed in a separate document, a link here will suffice.)

### 1. [Summary of critical path, e.g. 'Donations']

[Description of the overall functionality covered]

- Step-by-step instructions for what to test and what the expected behaviour is
- Include details for edge cases as well as the general case
- Break this into separate subsections if there's a lot to cover
- Don't include anything which is already covered by automated testing, unless it's a prerequisite for a manual test

## Other considerations

As well as testing the critical paths, these areas of functionality should be checked:

- ...
- Other places where you know extra maintenance or checks may be necessary
- This could be code which you know should be checked and possibly removed - e.g. because you've patched something until a fix is merged in a subsequent release.
- Any previous fixes which may need to be updated/reapplied on subsequent upgrades
- Technical debt which could be affected by an upgrade.
