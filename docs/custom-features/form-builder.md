# Formbuilder customisations

This project uses a custom `bc.forms` app that extends Wagtail's `contrib.forms`

## Submission auto-deletion

The `FormPage` model in `bc.forms` has a custom `auto_delete` field. When set to a non-zero value (zero is the default), form submissions for that form will be deleted after that many days.

This is done via a custom `stale_submissions` management command that's meant to be run daily.

## Embedded form blocks

There's a custom `EmbeddedFormBlock` that allows an editor to pick a `FormPage` and have the form for that page be embedded inside the streamfield.

The form submission is handled by the original `FormPage` view, so any validation error will be displayed on the non-embedded form page. Otherwise the form's submission is recorded and a "thank you" message (configurable) is displayed (embedded).
