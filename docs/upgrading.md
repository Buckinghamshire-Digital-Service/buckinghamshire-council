# Upgrading guidelines

This document describes aspects of the system which should be given particular attention when upgrading Wagtail or its dependencies.

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

## Forked Wagtail package dependencies

As much as possible, we want to use the official releases available on PyPI for the Wagtail package dependencies.

However, in certain situations, critical fixes and upgrades may be pending approval, merging, or release.
A temporary solution is to fork the package dependency, tag the working branch, and use the tag in the pyproject file.

The following packages are forked at the time of the latest upgrade (Wagtail 5.0):

- `wagtail-django-recaptcha`

Please note that it is important to replace the usage of the git tags in the pyproject.toml file with the official release version from PyPI as soon as it becomes available. This ensures that we maintain compatibility with the official releases and benefit from any subsequent updates and improvements provided by the original package maintainers.
