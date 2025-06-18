import pandas as pd
import xml.etree.ElementTree as et
from log.logger import log

def extract_from_csv(file):
    log(f"Starting CSV extraction from {file}")
    dataframe = pd.read_csv(file)
    log(f"Finished CSV extraction from {file}, {len(dataframe)} rows extracted")
    return dataframe

def extract_from_json(file):
    log(f"Starting JSON extraction from {file}")
    dataframe = pd.read_json(file, lines=True)
    log(f"Finished JSON extraction from {file}, {len(dataframe)} rows extracted")
    return dataframe

def extract_from_xml(file):
    log(f"Starting XML extraction from {file}")
    dataframe = pd.DataFrame(
        columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])

    tree = et.parse(file)
    root = tree.getroot()

    for car in root:
        car_model = car.find("car_model").text
        year_of_manufacture = int(car.find("year_of_manufacture").text)
        price = float(car.find("price").text)
        fuel = car.find("fuel").text
        # Use pd.concat instead of append for modern pandas
        new_row = pd.DataFrame([{
            "car_model": car_model,
            "year_of_manufacture": year_of_manufacture,
            "price": price,
            "fuel": fuel
        }])
        dataframe = pd.concat([dataframe, new_row], ignore_index=True)

    log(f"Finished XML extraction from {file}, {len(dataframe)} rows extracted")
    return dataframe
