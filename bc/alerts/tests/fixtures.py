import factory


class AlertFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "alerts.Alert"

    title = factory.Sequence(lambda n: f"Alert {n}")
