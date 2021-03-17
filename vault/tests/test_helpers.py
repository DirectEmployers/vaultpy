from base64 import b64encode
from unittest import TestCase

from vault import _is_base64


class SecretParsingTest(TestCase):
    def test_is_base64(self):
        test_string = "this will be base64 encoded"
        test_encoded = b64encode(bytes(test_string, "utf-8")).decode("utf-8")
        self.assertTrue(_is_base64(test_encoded))

    def test_is_not_base64(self):
        test_string = "this will be base64 encoded"
        self.assertFalse(_is_base64(test_string))
