import unittest
import pandas as pd
import os
import sys
import shutil # For rmtree
import xml.etree.ElementTree as ET

# Add parent directory to sys.path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extract.extract import extract_from_csv, extract_from_json, extract_from_xml

class TestExtractFunctions(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for test files."""
        self.temp_dir = "temp_test_data_extract"
        os.makedirs(self.temp_dir, exist_ok=True)

        self.expected_df = pd.DataFrame({
            'car_model': ['Civic', 'Accord'],
            'year_of_manufacture': [2019, 2020],
            'price': [20000.50, 25000.75],
            'fuel': ['Gasoline', 'Gasoline']
        })
        # Ensure correct dtypes for expected_df
        self.expected_df['year_of_manufacture'] = self.expected_df['year_of_manufacture'].astype('int64')
        self.expected_df['price'] = self.expected_df['price'].astype('float64')

    def tearDown(self):
        """Remove the temporary directory and its contents."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _create_sample_xml_file(self, filepath):
        xml_data = """
        <data>
            <car>
                <car_model>Civic</car_model>
                <year_of_manufacture>2019</year_of_manufacture>
                <price>20000.50</price>
                <fuel>Gasoline</fuel>
            </car>
            <car>
                <car_model>Accord</car_model>
                <year_of_manufacture>2020</year_of_manufacture>
                <price>25000.75</price>
                <fuel>Gasoline</fuel>
            </car>
        </data>
        """
        with open(filepath, 'w') as f:
            f.write(xml_data)

    def test_extract_from_csv(self):
        """Test extracting data from a CSV file."""
        csv_file_path = os.path.join(self.temp_dir, "sample.csv")
        # Create sample CSV file
        self.expected_df.to_csv(csv_file_path, index=False)

        extracted_df = extract_from_csv(csv_file_path)
        pd.testing.assert_frame_equal(extracted_df, self.expected_df)

    def test_extract_from_json(self):
        """Test extracting data from a JSON file (lines=True)."""
        json_file_path = os.path.join(self.temp_dir, "sample.json")
        # Create sample JSON file
        self.expected_df.to_json(json_file_path, orient='records', lines=True)

        extracted_df = extract_from_json(json_file_path)

        # JSON loader might infer int for price if .00, ensure consistency
        extracted_df['price'] = extracted_df['price'].astype('float64')
        extracted_df['year_of_manufacture'] = extracted_df['year_of_manufacture'].astype('int64')

        pd.testing.assert_frame_equal(extracted_df, self.expected_df)

    def test_extract_from_xml(self):
        """Test extracting data from an XML file."""
        xml_file_path = os.path.join(self.temp_dir, "sample.xml")
        self._create_sample_xml_file(xml_file_path)

        extracted_df = extract_from_xml(xml_file_path)

        # Ensure dtypes from XML extraction match expected
        extracted_df['year_of_manufacture'] = extracted_df['year_of_manufacture'].astype('int64')
        extracted_df['price'] = extracted_df['price'].astype('float64')

        # Sort by a column to ensure order doesn't affect comparison, if applicable
        # (The current extract_from_xml appends, so order should be preserved from XML file)
        # However, it's good practice if order is not guaranteed.
        expected_df_sorted = self.expected_df.sort_values(by='car_model').reset_index(drop=True)
        extracted_df_sorted = extracted_df.sort_values(by='car_model').reset_index(drop=True)

        # Ensure columns are in the same order
        extracted_df_sorted = extracted_df_sorted[expected_df_sorted.columns]

        pd.testing.assert_frame_equal(extracted_df_sorted, expected_df_sorted)

if __name__ == '__main__':
    unittest.main()
