import unittest
import pandas as pd
import os
import sys

# Add parent directory to sys.path to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transform.transform import transform_price, transform_to_upper

class TestTransformFunctions(unittest.TestCase):

    def setUp(self):
        """Set up sample data for transformation tests."""
        self.sample_df = pd.DataFrame({
            'car_model': ['Honda Civic', 'toyota camry'],
            'year_of_manufacture': [2019, 2020],
            'price': [20000.505, 25000.758], # Prices with >2 decimal places
            'fuel': ['Gasoline', 'hybrid']
        })
        # Ensure dtypes are as expected before transformation
        self.sample_df['car_model'] = self.sample_df['car_model'].astype(str)
        self.sample_df['year_of_manufacture'] = self.sample_df['year_of_manufacture'].astype('int64')
        self.sample_df['price'] = self.sample_df['price'].astype('float64')
        self.sample_df['fuel'] = self.sample_df['fuel'].astype(str)


    def test_transform_price(self):
        """Test rounding of the 'price' column to 2 decimal places."""
        transformed_df = transform_price(self.sample_df.copy()) # Use .copy() to avoid modifying original

        expected_prices = pd.Series([20000.51, 25000.76], name='price')
        pd.testing.assert_series_equal(transformed_df['price'], expected_prices, check_dtype=False)

        # Check that other columns remain unchanged
        expected_df = self.sample_df.copy()
        expected_df['price'] = expected_prices
        pd.testing.assert_frame_equal(transformed_df, expected_df)


    def test_transform_to_upper(self):
        """Test conversion of 'car_model' and 'fuel' columns to uppercase."""
        transformed_df = transform_to_upper(self.sample_df.copy()) # Use .copy()

        expected_car_models = pd.Series(['HONDA CIVIC', 'TOYOTA CAMRY'], name='car_model')
        expected_fuels = pd.Series(['GASOLINE', 'HYBRID'], name='fuel')

        pd.testing.assert_series_equal(transformed_df['car_model'], expected_car_models)
        pd.testing.assert_series_equal(transformed_df['fuel'], expected_fuels)

        # Check that other columns remain unchanged
        expected_df = self.sample_df.copy()
        expected_df['car_model'] = expected_car_models
        expected_df['fuel'] = expected_fuels
        pd.testing.assert_frame_equal(transformed_df, expected_df)

if __name__ == '__main__':
    unittest.main()
