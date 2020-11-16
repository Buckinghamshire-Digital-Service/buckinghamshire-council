from django.test import TestCase

from bc.search.tests.fixtures import TermFactory
from bc.search.utils import SYNONYMS_CACHE_KEY, cache, get_synonyms


class SynonymTest(TestCase):
    def test_basic(self):
        TermFactory(canonical_term="foo", synonyms=["soup", "potatoes"])
        self.assertListEqual(get_synonyms(force_update=True), ["foo, soup, potatoes"])

    def test_multi_word_phrase_synonym(self):
        TermFactory(
            canonical_term="foo",
            synonyms=["haircuts arguments", "small things", "rabbits"],
        )
        self.assertListEqual(
            get_synonyms(force_update=True),
            ["foo, haircuts arguments, small things, rabbits"],
        )

    def test_multi_word_canonical_term(self):
        TermFactory(
            canonical_term="people with noses", synonyms=["more jam", "soot", "flies"]
        )
        self.assertListEqual(
            get_synonyms(force_update=True),
            ["people with noses, more jam, soot, flies"],
        )

    def test_multiple_synonyms(self):
        TermFactory(canonical_term="foo", synonyms=["fish", "jam"])
        TermFactory(
            canonical_term="bar", synonyms=["tobogganing", "showers", "toasters"]
        )
        self.assertListEqual(
            get_synonyms(force_update=True),
            ["foo, fish, jam", "bar, tobogganing, showers, toasters"],
        )

    def test_synonyms_are_lower_cased(self):
        TermFactory(canonical_term="foo", synonyms=["Belgium", "fire", "water"])
        self.assertListEqual(
            get_synonyms(force_update=True), ["foo, belgium, fire, water"]
        )

    def test_synonyms_are_cached(self):
        TermFactory(canonical_term="foo", synonyms=["light", "air"])
        self.assertListEqual(get_synonyms(force_update=True), ["foo, light, air"])
        self.assertListEqual(cache.get(SYNONYMS_CACHE_KEY), ["foo, light, air"])

    def test_cache_is_used(self):
        cache.set(SYNONYMS_CACHE_KEY, ["foo, eggnog, radiators"])
        self.assertListEqual(get_synonyms(), ["foo, eggnog, radiators"])

        TermFactory(canonical_term="bar", synonyms=["grandmothers"])
        self.assertListEqual(get_synonyms(), ["foo, eggnog, radiators"])  # unchanged
        self.assertListEqual(get_synonyms(force_update=True), ["bar, grandmothers"])
