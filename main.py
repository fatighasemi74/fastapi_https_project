from fastapi import FastAPI, HTTPException, Depends
import httpx

app = FastAPI()

async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/posts")
async def get_posts(client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get("https://jsonplaceholder.typicode.com/posts")
    return response.json()


@app.get("/posts/{post_id}")
async def get_post(post_id: int, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Post not found")
    return response.json()