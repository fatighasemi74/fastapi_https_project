from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx


app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/posts", response_class=HTMLResponse)
async def get_posts(request: Request, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get("https://jsonplaceholder.typicode.com/posts")
    return templates.TemplateResponse("posts.html", {"request": request, "posts": response.json()})


@app.get("/posts/{post_id}", response_class=HTMLResponse)
async def get_post(request: Request, post_id: int, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Post not found")
    post = response.json()
    return templates.TemplateResponse("post.html", {"request": request, "post": post})