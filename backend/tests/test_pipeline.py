from unittest.mock import patch
import pytest

from etl.pipeline import run_etl_pipeline


def test_pipeline_success():
    with patch('etl.pipeline.extract') as mock_extract, \
         patch('etl.pipeline.transform') as mock_transform, \
         patch('etl.pipeline.load') as mock_load:
        
        mock_extract.return_value = "<xml>fake data</xml"
        mock_transform.return_value = (
            "2099-01-01",
            [{"currency": "USD", "value": 4.55, "date": "2099-01-01"}],
            {"total_records": 1, "valid_records": 1, "invalid_records": 0}
        )
        mock_load.return_value = 1

        result = run_etl_pipeline()

        assert result["status"] =="success"
        assert result["date"] == "2099-01-01"
        assert result["records_extracted"] == 1
        assert result["records_valid"] == 1
        assert result["records_invalid"] == 0
        assert result["records_loaded"] == 1
        assert "duration_seconds" in result

def test_pipeline_failure():
    with patch('etl.pipeline.extract') as mock_extract:
        mock_extract.side_effect = Exception("API is down")

        result = run_etl_pipeline()

        assert result["status"] == "failure"
        assert "API is down" in result["error"]
        assert "duration_seconds" in result
