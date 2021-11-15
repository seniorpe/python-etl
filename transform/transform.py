def transform_price(data):
       data['price'] = round(data.price, 2)
       return data

def transform_to_upper(data):
       data['car_model'] = data.car_model.str.upper()
       data['fuel'] = data.fuel.str.upper()
       
       return data