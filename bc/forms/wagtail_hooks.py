from wagtail import hooks

from .models import FormSubmissionAccessControl


def _user_can_see_submissions(user):
    groups_with_access = FormSubmissionAccessControl.load().groups_with_access.all()
    return user.groups.filter(pk__in=groups_with_access).exists()


@hooks.register("filter_form_submissions_for_user")
def restrict_submissions(user, queryset):
    if user.is_superuser or _user_can_see_submissions(user):
        return queryset
    else:
        return queryset.none()
