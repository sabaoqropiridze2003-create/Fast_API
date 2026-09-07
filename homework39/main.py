from fastapi import FastAPI, HTTPException, status
from schemas import ProductCreateRequest, ProductResponse

app = FastAPI()

products_db = []
product_id_counter = 1


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreateRequest):
    global product_id_counter

    product_data = product.model_dump()
    product_data["id"] = product_id_counter

    products_db.append(product_data)
    product_id_counter += 1

    return product_data


@app.get("/products", response_model=list[ProductResponse])
def get_all_products():
    return products_db


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")