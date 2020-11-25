from unittest.mock import patch

from django.test import TestCase

from bc.search.tests.fixtures import TermFactory
from bc.search.utils import SYNONYMS_CACHE_KEY, cache, get_synonyms


class SynonymTest(TestCase):
    def test_basic(self):
        TermFactory(canonical_term="foo", synonyms=["soup", "potatoes"])
        self.assertListEqual(get_synonyms(), ["foo, soup, potatoes"])

    def test_multi_word_phrase_synonym(self):
        TermFactory(
            canonical_term="foo",
            synonyms=["haircuts arguments", "small things", "rabbits"],
        )
        self.assertListEqual(
            get_synonyms(), ["foo, haircuts arguments, small things, rabbits"],
        )

    def test_multi_word_canonical_term(self):
        TermFactory(
            canonical_term="people with noses", synonyms=["more jam", "soot", "flies"]
        )
        self.assertListEqual(
            get_synonyms(), ["people with noses, more jam, soot, flies"],
        )

    def test_multiple_synonyms(self):
        TermFactory(canonical_term="foo", synonyms=["fish", "jam"])
        TermFactory(
            canonical_term="bar", synonyms=["tobogganing", "showers", "toasters"]
        )
        self.assertListEqual(
            get_synonyms(), ["foo, fish, jam", "bar, tobogganing, showers, toasters"],
        )

    def test_synonyms_are_lower_cased(self):
        TermFactory(canonical_term="foo", synonyms=["Belgium", "fire", "water"])
        self.assertListEqual(get_synonyms(), ["foo, belgium, fire, water"])

    @patch("bc.search.signal_handlers.get_synonyms")
    def test_signal_is_triggered(self, mock_get_synonyms):
        TermFactory(canonical_term="foo", synonyms=["lights", "Burma"])
        mock_get_synonyms.assert_called_once_with(force_update=True)

    def test_synonyms_are_cached(self):
        cache.delete(SYNONYMS_CACHE_KEY)
        self.assertEqual(cache.get(SYNONYMS_CACHE_KEY), None)

        TermFactory(canonical_term="foo", synonyms=["light", "air"])
        self.assertListEqual(cache.get(SYNONYMS_CACHE_KEY), ["foo, light, air"])

    def test_synonym_cache_can_be_updated(self):
        TermFactory(
            canonical_term="foo", synonyms=["things that go 'uhh'", "Arthur Negus"]
        )
        cache.set(SYNONYMS_CACHE_KEY, ["foo, colonel gaddafi"])
        self.assertListEqual(cache.get(SYNONYMS_CACHE_KEY), ["foo, colonel gaddafi"])
        self.assertListEqual(
            get_synonyms(force_update=True), ["foo, things that go 'uhh', arthur negus"]
        )
        self.assertListEqual(
            cache.get(SYNONYMS_CACHE_KEY), ["foo, things that go 'uhh', arthur negus"]
        )

    def test_cache_is_used(self):
        cache.set(SYNONYMS_CACHE_KEY, ["foo, eggnog, radiators"])
        self.assertListEqual(get_synonyms(), ["foo, eggnog, radiators"])

        TermFactory(canonical_term="bar", synonyms=["grandmothers"])
        self.assertListEqual(get_synonyms(), ["bar, grandmothers"])
