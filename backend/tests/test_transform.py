#Project/backend/tests/test_transform.py

from etl.transform import transform

def test_transform_valid_data():
    raw_xml = """
    <DataSet>
        <Body>
            <Cube date="2026-03-07">
                <Rate currency="USD">4.55</Rate>
                <Rate currency="EUR">4.98</Rate>
            </Cube>
        </Body>
    </DataSet>
    """

    bnr_date, structured_rates, metrics = transform(raw_xml)

    assert bnr_date == "2026-03-07"
    assert len(structured_rates) == 2
    assert metrics["total_records"] == 2
    assert metrics["valid_records"] == 2
    assert metrics["invalid_records"] == 0


def test_transform_skips_negative_rate():
    raw_xml = """
    <DataSet>
        <Body>
            <Cube date="2026-03-07">
                <Rate currency="USD">-4.55</Rate>
                <Rate currency="EUR">4.98</Rate>
            </Cube>
        </Body>
    </DataSet>
    """

    bnr_date, structured_rates, metrics = transform(raw_xml)

    assert bnr_date == "2026-03-07"
    assert len(structured_rates) == 1
    assert structured_rates[0]["currency"] == "EUR"
    assert metrics["total_records"] == 2
    assert metrics["valid_records"] == 1
    assert metrics["invalid_records"] == 1


def test_transform_skips_invalid_currency_name():
    raw_xml = """
    <DataSet>
        <Body>
            <Cube date="2026-03-07">
                <Rate currency="US">-4.55</Rate>
                <Rate currency="EUR">4.98</Rate>
            </Cube>
        </Body>
    </DataSet>
    """

    bnr_date, structured_rates, metrics = transform(raw_xml)

    assert bnr_date == "2026-03-07"
    assert len(structured_rates) == 1
    assert structured_rates[0]["currency"] == "EUR"
    assert metrics["total_records"] == 2
    assert metrics["valid_records"] == 1
    assert metrics["invalid_records"] == 1
