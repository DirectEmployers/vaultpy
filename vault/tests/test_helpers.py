from base64 import b64encode
from json import dumps
from unittest import TestCase

from vault import _is_base64, _parse_json_secrets


class HelperFunctionsTest(TestCase):
    def test_is_base64(self):
        test_string = "this will be base64 encoded"
        test_encoded = b64encode(bytes(test_string, "utf-8")).decode("utf-8")
        self.assertTrue(_is_base64(test_encoded))

    def test_is_not_base64(self):
        test_string = "this will be base64 encoded"
        self.assertFalse(_is_base64(test_string))

    def test_json_parsing(self):
        """
        JSON objects may by simple key -> value objects, or adhere to some form of
        Vault's own Secret struct format (which nests object content in `data` objects).
        """
        plain_secret = {"SECRET_KEY": "secret value"}
        data_secret = {"data": plain_secret}
        ddata_secret = {"data": data_secret}

        # Not a thing, should yield a dict that looks like {data: {SECRET_KEY: ...}}.
        dddata_secret = {"data": ddata_secret}

        # Tests expected test cases where secrets are either top level or under up to
        # two levels of `data` keys.
        for secrets in [plain_secret, data_secret, ddata_secret]:
            secrets = dumps(secrets)
            parsed = _parse_json_secrets(secrets)
            self.assertEqual(plain_secret, parsed)

        # Tests the case where our expected secrets are under three levels of `data`
        # keys, which would result in `data` being a top-level dictionary key.
        secrets = dumps(dddata_secret)
        parsed = _parse_json_secrets(secrets)
        self.assertEqual(data_secret, parsed)
