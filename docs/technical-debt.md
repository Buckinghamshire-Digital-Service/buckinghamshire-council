# Technical debt

This page describes known technical debt or shortcomings in the project.

## Non-family info sites and pages using `family_info` Django application's code

There are subsites set up using `family_info` Django application's models that are not family info subsite.

A likely good idea would be to refactor the `family_info` Django application to be more generic
and move the family info specific code to a separate Django application.

This may be especially confusing for new developers trying to find their way in the codebase.

Short-term actions to address:

- Any FIS-named code should be reviewed and checked if it should be called something else.
- Add comments around FIS-named things whether they are actually FIS-specific.
- Document this somewhere else

Ideally:

- Formulate plan for renaming the code.
- Migrate existing subsites to use generic, non-FIS code as much as possible.
- Any new subsites should use generic, non-FIS code only.

We don't want to be in situation where FIS-specific code is used for non-FIS subsites.
