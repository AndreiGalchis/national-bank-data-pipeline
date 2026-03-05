#backend/etl/transform.py

import xmltodict
import logging
from datetime import datetime

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class BNRTransformer:

    @staticmethod
    def parse_xml(xml_data: str):
        try:
            parsed = xmltodict.parse(xml_data)
            logger.info("XML data parsed successfully")
            return parsed
        except Exception as e:
            logger.error(f"Failed to parse XML data: {e}")
            raise

    @staticmethod
    def extract_date_and_list_of_rates(parsed_xml):
        body = parsed_xml["DataSet"]["Body"]
        cube = body["Cube"]
        bnr_date = cube["@date"]
        rates = cube["Rate"]
        logger.info(f"Found {len(rates)} rates for {bnr_date}")
        return bnr_date, rates
    
    @staticmethod
    def validate_and_structure_rates(bnr_date: str, rates):

        datetime.strptime(bnr_date, "%Y-%m-%d")

        structured = []
        for r in rates:
            structured.append({
                "currency": r["@currency"].upper(),
                "value": float(r["#text"]),
                "date": bnr_date
            })

        logger.info(f"Structured {len(structured)} rates for {bnr_date}")
        return structured
    
def transform(raw_xml: str):
        
    transformer = BNRTransformer()
    parsed_xml = transformer.parse_xml(raw_xml)
    bnr_date, raw_rates = transformer.extract_date_and_list_of_rates(parsed_xml)
    structured_rates = transformer.validate_and_structure_rates(bnr_date, raw_rates)
    return bnr_date, structured_rates
    

