import pandas as pd
import xml.etree.ElementTree as ET
from log.logger import log

def save_to_csv(df: pd.DataFrame, path: str):
    """Saves a DataFrame to a CSV file."""
    log(f"Starting CSV load to {path}")
    df.to_csv(path, index=False)
    log(f"Finished CSV load to {path}")

def save_to_json(df: pd.DataFrame, path: str):
    """Saves a DataFrame to a JSON file."""
    log(f"Starting JSON load to {path}")
    df.to_json(path, orient='records', lines=True)
    log(f"Finished JSON load to {path}")

def save_to_xml(df: pd.DataFrame, path: str):
    """Saves a DataFrame to an XML file."""
    log(f"Starting XML load to {path}")
    root = ET.Element("data")

    for _, row in df.iterrows():
        car_element = ET.SubElement(root, "car")
        for col in df.columns:
            # Ensure value is not None before converting to string
            cell_value = row[col]
            ET.SubElement(car_element, col).text = str(cell_value) if cell_value is not None else ""

    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)
    log(f"Finished XML load to {path}")
