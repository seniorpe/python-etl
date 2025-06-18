# Building ETL (Extract, Transform, Load) in Python 
##### What is ETL (Extract, Transform, Load)?
Extract, transform, and load (ETL) is a data integration methodology that extracts raw data from sources, transforms the data on a secondary processing server, and then loads the data into a target database.

![](_screenshots/etl.png)

# Requirements
You will need the following software:
- `glob`, a package that is preinstalled that searches for files in relative paths.
For details, see this [section](https://docs.python.org/3/library/glob.html "section") for documentation.
- `pandas`, a package used for data manipulation. To install, type on the command line, `pip install pandas`.
For details, see the [pandas](https://pandas.pydata.org/ "pandas") site.

# Project Structure
This project is organized into several key directories:
-   `extract/`: Contains scripts for extracting data from various source file formats (CSV, JSON, XML).
-   `transform/`: Holds scripts for transforming the extracted data (e.g., data type conversion, value modification).
-   `load/`: Includes scripts for loading the transformed data into different output file formats.
-   `data/`: This directory is split into:
    -   `data/source/`: Contains the source data files to be processed by the ETL pipeline.
    -   `data/target/`: The destination for the transformed data files.
-   `tests/`: Contains all unit tests for the project, ensuring code reliability.
-   `log/`: Contains the logging configuration (`logger.py`) and the log output file.

# Running the ETL Pipeline
The ETL pipeline is designed to process all compatible source files (CSV, JSON, XML) found within the `data/source/` directory.

To run the ETL pipeline, navigate to the root directory of the project in your terminal and execute:
```bash
python __init__.py
```

# Output
After a successful run, the transformed data is saved into the `data/target/` directory. The pipeline generates output in the following formats:
-   `car_prices_transformed.csv`
-   `car_prices_transformed.json`
-   `car_prices_transformed.xml`

# Logging
The pipeline logs its operations and progress, providing insights into the ETL process.
Logs are saved to `log.log` in the root directory of the project.

# Testing
Unit tests have been implemented to ensure the functionality of individual components of the ETL pipeline.
-   Unit tests are located in the `tests/` directory.
-   To run the tests, navigate to the root directory and execute the following command:
    ```bash
    python -m unittest discover tests
    ```
