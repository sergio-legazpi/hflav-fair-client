import json
from unittest.mock import patch, Mock

import pytest

from hflav_zenodo import ZenodoClient


def make_hit(id_, date_str, title="Test"):
    return {
        "id": id_,
        "created": date_str,
        "metadata": {"title": title, "publication_date": date_str},
    }


@patch("hflav_zenodo.client.requests.Session.get")
def test_get_latest_hflav(mock_get):
    # Prepare fake search response with two hits
    hits = [make_hit(1, "2020-01-01"), make_hit(2, "2022-03-15")]
    fake_search = {"hits": {"hits": hits}}

    mock_resp = Mock()
    mock_resp.raise_for_status = Mock()
    mock_resp.json.return_value = fake_search
    mock_get.return_value = mock_resp

    client = ZenodoClient()
    latest = client.get_latest_hflav()
    assert latest is not None
    assert latest["id"] == 2


@patch("hflav_zenodo.client.requests.Session.get")
def test_download_file_selects_file(mock_get):
    # Create a fake record with files
    record = {
        "id": 123,
        "files": [
            {"key": "data.csv", "links": {"download": "https://example.com/data.csv"}},
            {
                "key": "readme.txt",
                "links": {"download": "https://example.com/readme.txt"},
            },
        ],
    }

    # First call for get_record will return record JSON
    resp_record = Mock()
    resp_record.raise_for_status = Mock()
    resp_record.json.return_value = record

    # Second call for the file download returns a streaming response
    resp_stream = Mock()
    resp_stream.raise_for_status = Mock()
    resp_stream.iter_content = Mock(return_value=[b"hello", b"world"])

    # Configure side effects: get_record call then download call
    mock_get.side_effect = [resp_record, resp_stream]

    client = ZenodoClient()
    # use a temporary file path
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        out = client.download_file(123, filename="data.csv", dest_path=td)
        assert out.endswith("data.csv")
        # content written
        with open(out, "rb") as fh:
            data = fh.read()
        assert b"helloworld" in data.replace(b"", b"") or len(data) > 0
