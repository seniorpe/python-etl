import glob
import os
import pandas as pd

from log.logger import log
import extract.extract as e
import transform.transform as t
import load.load as l

log("ETL Job Started")

# --- Extraction Phase ---
log("Extract phase Started")
all_dataframes = []
source_files_csv = glob.glob("data/source/*.csv")
source_files_json = glob.glob("data/source/*.json")
source_files_xml = glob.glob("data/source/*.xml")
all_source_files = source_files_csv + source_files_json + source_files_xml

log(f"Found the following source files: {all_source_files}")

for filepath in all_source_files:
    log(f"Processing file: {filepath}")
    if filepath.endswith('.csv'):
        df = e.extract_from_csv(filepath)
    elif filepath.endswith('.json'):
        df = e.extract_from_json(filepath)
    elif filepath.endswith('.xml'):
        df = e.extract_from_xml(filepath)
    else:
        log(f"Unsupported file type: {filepath}")
        continue
    if df is not None: # Ensure df is not None before appending
        all_dataframes.append(df)
    else:
        log(f"No data extracted from {filepath}")


if not all_dataframes:
    log("No data found in source files. ETL process will result in empty target files.")
    extracted_data = pd.DataFrame()
else:
    extracted_data = pd.concat(all_dataframes, ignore_index=True)

log(f"Successfully concatenated {len(all_dataframes)} dataframes. Total rows: {len(extracted_data)}")
log("Extract phase Ended")

# --- Transformation Phase ---
log("Transform phase Started")
if not extracted_data.empty:
    transformed_data = t.transform_price(extracted_data.copy())
    transformed_data = t.transform_to_upper(transformed_data)
else:
    log("Skipping transformation as extracted data is empty.")
    transformed_data = pd.DataFrame() # Pass an empty DataFrame
log("Transform phase Ended")

# --- Loading Phase ---
log("Load phase Started")
os.makedirs("data/target", exist_ok=True)

target_csv_file = "data/target/car_prices_transformed.csv"
target_json_file = "data/target/car_prices_transformed.json"
target_xml_file = "data/target/car_prices_transformed.xml"

log(f"Saving transformed data to CSV: {target_csv_file}")
l.save_to_csv(transformed_data, target_csv_file)

log(f"Saving transformed data to JSON: {target_json_file}")
l.save_to_json(transformed_data, target_json_file)

log(f"Saving transformed data to XML: {target_xml_file}")
l.save_to_xml(transformed_data, target_xml_file)

log("Load phase Ended")
log("ETL Job Ended")
