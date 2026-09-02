from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
def get_all_products():
    return {"message": "retrieved succsessfully"}

@app.post("/products")
def create_product(product: dict):
    return {"message": "created product", "product": product}

@app.put("/update")
def update_product(new_product: dict):
    return {"message": "updated product", "product": new_product}

@app.patch("/update_item")
def patch_product(new_product: dict):
    return {"message": "updated product", "product": new_product}

@app.delete("/delete_item")
def delete_product(id: int):
    return {"message": "deleted product", "deleted product with id": id}