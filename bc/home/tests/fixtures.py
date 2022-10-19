import factory


class HomePageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "home.HomePage"

    title = factory.Sequence(lambda n: f"Homepage {n}")
    strapline = "Welcome to Buckinghamshire"
    listing_summary = "Welcome to Buckinghamshire"
    hero_image = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")
    logo = factory.SubFactory("bc.images.tests.fixtures.ImageFactory")

    @classmethod
    def build_with_fk_objs_committed(cls, **kwargs):
        from bc.images.tests.fixtures import ImageFactory

        image = ImageFactory()
        return cls.build(hero_image=image, logo=image, **kwargs)
