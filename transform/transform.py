from log.logger import log
import pandas as pd # Ensure pandas is imported

def transform_price(data):
    log("Starting price transformation")
    if 'price' in data.columns:
        # Ensure 'price' is numeric before rounding, coercing errors
        data['price'] = pd.to_numeric(data['price'], errors='coerce')
        # Pandas Series round method is generally preferred for Series objects
        data['price'] = data['price'].round(2)
    else:
        log("Warning: 'price' column not found. Skipping price transformation.")
    log("Finished price transformation")
    return data

def transform_to_upper(data):
    log("Starting case transformation to uppercase for car_model and fuel")
    if 'car_model' in data.columns:
        # Ensure 'car_model' is of string type before using .str accessor
        data['car_model'] = data['car_model'].astype(str).str.upper()
    else:
        log("Warning: 'car_model' column not found. Skipping case transformation for car_model.")

    if 'fuel' in data.columns:
        # Ensure 'fuel' is of string type before using .str accessor
        data['fuel'] = data['fuel'].astype(str).str.upper()
    else:
        log("Warning: 'fuel' column not found. Skipping case transformation for fuel.")

    log("Finished case transformation")
    return data