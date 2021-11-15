import pandas as pd
import xml.etree.ElementTree as et


def extract_from_csv(file):
    dataframe = pd.read_csv(file)
    return dataframe


def extract_from_json(file):
    dataframe = pd.read_json(file, lines=True)
    return dataframe


def extract_from_xml(file):

    dataframe = pd.DataFrame(
        columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])

    tree = et.parse(file)
    root = tree.getroot()

    for car in root:
        car_model = car.find("car_model").text
        year_of_manufacture = int(car.find("year_of_manufacture").text)
        price = float(car.find("price").text)
        fuel = car.find("fuel").text
        dataframe = dataframe.append({"car_model": car_model,
                                      "year_of_manufacture": year_of_manufacture,
                                      "price": price,
                                      "fuel": fuel
                                      }, ignore_index=True)

    return dataframe
