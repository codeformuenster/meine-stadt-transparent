import pytest
import responses
from django.test import TestCase

from requests.exceptions import ConnectionError
from importer.loader import SternbergLoader


class TestSternberg(TestCase):
    """ Tests for the workaround for the bugs in Sterberg's OParl implementation

    The exact urls might not return an error anymore, but any timestamp in the future will work
    """

    def test_empty_list_returns_error(self):
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.GET,
                "https://ris.krefeld.de/webservice/oparl/v1.0/body/1/paper?modified_since=2019-05-30T22%3A00%3A08.100505%2B00%3A00",
                content_type="text/html",
                status=404,
                body='{"error":"Die angeforderte Ressource wurde nicht gefunden.","code":802,"type":"SD.NET RIM Webservice"}',
            )

            loader = SternbergLoader({})
            data = loader.load(
                "https://ris.krefeld.de/webservice/oparl/v1.0/body/1/paper",
                query={"modified_since": "2019-05-30T22:00:08.100505+00:00"},
            )

            self.assertEqual(data["data"], [])

            with pytest.raises(ConnectionError):
                loader.load("https://ris.krefeld.de/webservice/oparl/v1.0/body/1/paper")

    def test_empty_list_should_have_been_object(self):
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.GET,
                "https://ris.krefeld.de/webservice/oparl/v1.0/body/1/meeting?modified_since=2019-05-09T20%3A51%3A54.198089%2B00%3A00",
                json=[],
            )

            loader = SternbergLoader({})
            data = loader.load(
                "https://ris.krefeld.de/webservice/oparl/v1.0/body/1/meeting",
                query={"modified_since": "2019-05-09T20:51:54.198089+00:00"},
            )

            self.assertTrue("data" in data)
            self.assertEqual(data["data"], [])

            with pytest.raises(ConnectionError):
                loader.load(
                    "https://ris.krefeld.de/webservice/oparl/v1.0/body/1/meeting"
                )

    def test_deleted_missing_type(self):
        data = {
            "id": "https://ris.krefeld.de/webservice/oparl/v1.0/body/1/file/2-19309",
            "created": "2019-03-19T09:59:05+01:00",
            "modified": "2019-04-16T09:02:31+02:00",
            "deleted": True,
        }

        with responses.RequestsMock() as requests_mock:
            requests_mock.add(requests_mock.GET, data["id"], json=data)

            loader = SternbergLoader({})
            data = loader.load(data["id"])

            self.assertEqual(data["type"], "https://schema.oparl.org/1.0/File")

    def test_mixed_up_extensions(self):
        url_wrong = "https://oparl.example.org/download/file.eml.eml"
        url_correct = "https://oparl.example.org/download/file.eml.pdf"

        with responses.RequestsMock() as requests_mock:
            requests_mock.add(requests_mock.GET, url_wrong, status=404)
            requests_mock.add(requests_mock.GET, url_correct, body=b"OK")

            loader = SternbergLoader({})
            content, content_type = loader.load_file(url_wrong)
            self.assertEqual(content, b"OK")
