from log.logger import log

import extract as e
import transform as t
import load as l

target_file = "data/target/data.csv"   # transformed data is stored

log("ETL Job Started")
log("Extract phase Started")
extracted_data = e.extract()
log("Extract phase Ended")

log("Transform phase Started")
transformed_data = t.transform(extracted_data)
log("Transform phase Ended")

log("Load phase Started")
l.load(target_file, transformed_data)
log("Load phase Ended")
log("ETL Job Ended")