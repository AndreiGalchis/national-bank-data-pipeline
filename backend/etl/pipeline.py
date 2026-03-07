# backend/etl/pipeline.py

import logging
from datetime import datetime

from etl.extract import extract
from etl.transform import transform
from etl.load import load

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class ETLPipeline:

    @staticmethod
    def run(source = "bnr"):

        start_time = datetime.now()

        logger.info("=" * 60)
        logger.info("Starting ETL Pipeline")
        logger.info("=" * 60)

        try:
            # EXTRACT
            logger.info("\n EXTRACT - Fetching data...")
            raw_data = extract(source = source)
            logger.info("Extract completed")

            # TRANSFORM
            logger.info("\n TRANSFORM - Processing data...")
            date_str, structured_rates, transform_metrics = transform(raw_data)
            logger.info(f"Transform completed - {len(structured_rates)} records")

            # LOAD
            logger.info("\n LOAD- Saving to database...")
            records_loaded = load(date_str, structured_rates)
            logger.info(f"Load completed - {records_loaded} records saved")

            # CALCULATE DURATION
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("=" * 60)
            logger.info(f"Pipeline completed in {duration:.2f}s")
            logger.info("=" * 60 + "\n")

            return {
                "status": "success",
                "date": date_str,
                "records_extracted": transform_metrics["total_records"],
                "records_valid": transform_metrics["valid_records"],
                "records_invalid": transform_metrics["invalid_records"],
                "records_loaded": records_loaded,
                "duration_seconds": duration
            }
        
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info("=" * 60)
            logger.info(f"Pipeline failed: {e}")
            logger.info("=" * 60 + "\n")

            return {
                "status": "failure",
                "error": str(e),
                "duration_seconds": duration
            }


def run_etl_pipeline(source="bnr"):

    return ETLPipeline.run(source=source)
    
