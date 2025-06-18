import unittest
import pandas as pd
import os
import xml.etree.ElementTree as ET
import sys

# Add parent directory to sys.path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Correct import for functions from load/load.py:
from load.load import save_to_csv, save_to_json, save_to_xml

class TestLoadFunctions(unittest.TestCase):

    def setUp(self):
        """Set up sample data and temporary file paths for tests."""
        self.sample_df = pd.DataFrame({
            'car_model': ['Model S', 'Model 3'],
            'year_of_manufacture': [2020, 2021],
            'price': [79999.00, 39999.00], # Ensure price is float
            'fuel': ['Electric', 'Electric']
        })
        self.temp_csv_file = "test_output.csv"
        self.temp_json_file = "test_output.json"
        self.temp_xml_file = "test_output.xml"

    def tearDown(self):
        """Clean up temporary files after each test."""
        if os.path.exists(self.temp_csv_file):
            os.remove(self.temp_csv_file)
        if os.path.exists(self.temp_json_file):
            os.remove(self.temp_json_file)
        if os.path.exists(self.temp_xml_file):
            os.remove(self.temp_xml_file)

    def test_save_to_csv(self):
        """Test saving DataFrame to CSV and verifying its content."""
        save_to_csv(self.sample_df, self.temp_csv_file) # Corrected call
        loaded_df = pd.read_csv(self.temp_csv_file)
        # Ensure data types are consistent for comparison, esp. for float
        self.sample_df['price'] = self.sample_df['price'].astype('float64')
        loaded_df['price'] = loaded_df['price'].astype('float64')
        pd.testing.assert_frame_equal(loaded_df, self.sample_df)

    def test_save_to_json(self):
        """Test saving DataFrame to JSON and verifying its content."""
        save_to_json(self.sample_df, self.temp_json_file) # Corrected call
        loaded_df = pd.read_json(self.temp_json_file, orient='records', lines=True)

        # Ensure data types are consistent, especially for floats and potentially integers
        expected_df = self.sample_df.copy()
        expected_df['price'] = expected_df['price'].astype('float64')
        # year_of_manufacture might be read as int64 by default if only ints, which is fine
        # loaded_df might read numeric columns that look like int as int
        loaded_df['price'] = loaded_df['price'].astype('float64')
        loaded_df['year_of_manufacture'] = loaded_df['year_of_manufacture'].astype('int64')
        expected_df['year_of_manufacture'] = expected_df['year_of_manufacture'].astype('int64')


        pd.testing.assert_frame_equal(loaded_df, expected_df)

    def test_save_to_xml(self):
        """Test saving DataFrame to XML and verifying its content."""
        save_to_xml(self.sample_df, self.temp_xml_file) # Corrected call

        # Parse the XML and reconstruct DataFrame
        tree = ET.parse(self.temp_xml_file)
        root = tree.getroot()

        data_list = []
        for car_element in root.findall("car"):
            data = {}
            for child in car_element:
                data[child.tag] = child.text
            data_list.append(data)

        loaded_df = pd.DataFrame(data_list)

        # Ensure correct dtypes for comparison
        expected_df = self.sample_df.copy()
        loaded_df['year_of_manufacture'] = loaded_df['year_of_manufacture'].astype('int64')
        loaded_df['price'] = loaded_df['price'].astype('float64')
        # car_model and fuel are objects (strings), which is usually fine by default

        # Columns in XML might be read in different order, sort before comparison
        expected_df = expected_df.sort_values(by='car_model').reset_index(drop=True)
        loaded_df = loaded_df.sort_values(by='car_model').reset_index(drop=True)

        # Reorder columns of loaded_df to match expected_df for assert_frame_equal
        loaded_df = loaded_df[expected_df.columns]

        pd.testing.assert_frame_equal(loaded_df, expected_df)

if __name__ == '__main__':
    unittest.main()
