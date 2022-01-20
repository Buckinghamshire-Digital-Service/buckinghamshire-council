import wagtail_factories


class StepByStepPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = "step_by_step.StepByStepPage"

    introduction = "<p>Introduction</p>"
