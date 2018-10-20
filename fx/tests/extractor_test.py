from unittest import TestCase

from feature_extraction import extractor


class ExtractorTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_dir = 'tests/fixtures'
        cls.invalid_dir = './not_a_real_directory'

    def test_validate_dir_valid(self):
        self.assertEqual(
                extractor._validate_dir(self.fixture_dir), self.fixture_dir,
                'validate_dir should return the passed in string if it is a valid directory')

    def test_validate_dir_invalid(self):
        with self.assertRaises(Exception):
            extractor._validate_dir(self.invalid_fixture_dir)
