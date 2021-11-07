import unittest

from hajimari.utils import slugify


class TestUtils(unittest.TestCase):

    def test_slugify(self):
        result = slugify("Example name with spaces")
        self.assertEqual("example-name-with-spaces", result)

    def test_slugify2(self):
        result = slugify("example_ml_service")
        self.assertEqual("example_ml_service", result)


if __name__ == '__main__':
    unittest.main()
