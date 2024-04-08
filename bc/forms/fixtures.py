import factory


class PostcodeLookupResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "forms.PostcodeLookupResponse"

    answer = "The answer"
    postcodes = ["HP20 1UY"]


class LookupPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "forms.LookupPage"

    title = factory.Sequence(lambda n: "Lookup Response Page")
    listing_summary = "Lookup Response Page"
    form_heading = "Look something up"
    input_label = "Submit this query"
    input_help_text = "This tells you to submit this query"
    no_match_message = "There is no match"
    start_again_text = "Start again"

    # responses = factory.SubFactory("bc.forms.fixtures.PostcodeLookupResponseFactory")
