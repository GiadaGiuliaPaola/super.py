import uuid

#for every product generate a unique identifier number
def generate_product_id():
    new_id = str(uuid.uuid4())[-4:] 
    return new_id
