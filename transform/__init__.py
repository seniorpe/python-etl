from transform.transform import transform_price, transform_to_upper

def transform(data):
    data = transform_price(data)
    return transform_to_upper(data)
