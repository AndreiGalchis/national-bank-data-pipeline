#backend/etl/extract.py

import requests
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

BNR_URL = "https://www.bnr.ro/nbrfxrates.xml"


class BNRExtractor:

    @staticmethod
    def fetch_bnr_xml():
        try:
            logger.info(f"Fetching BNR data from: {BNR_URL}")
            response = requests.get(BNR_URL)
            response.raise_for_status()
            logger.info("BNR data fetched successfully")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch BNR data: {e}")
            raise


def extract(source="bnr"):
    if source.lower() == "bnr":
        return BNRExtractor.fetch_bnr_xml()
    else:
        raise ValueError(f"Unknown source: {source}")
        
    
     