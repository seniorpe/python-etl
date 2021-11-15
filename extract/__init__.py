import glob
import pandas as pd

from extract.extract import extract_from_csv, extract_from_json, extract_from_xml

def extract():
    extracted_data = pd.DataFrame(
        columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])

    for csvfile in glob.glob("data/source/*.csv"):
        extracted_data = extracted_data.append(
            extract_from_csv(csvfile), ignore_index=True)

    for jsonfile in glob.glob("data/source/*.json"):
        extracted_data = extracted_data.append(
            extract_from_json(jsonfile), ignore_index=True)

    for xmlfile in glob.glob("data/source/*.xml"):
        extracted_data = extracted_data.append(
            extract_from_xml(xmlfile), ignore_index=True)

    return extracted_data
