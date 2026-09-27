import time
async def log_request(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    print(f"Request: {request.method} {request.url.path}, Client host: {request.client.host} - {process_time:.4f} seconds")

    return response