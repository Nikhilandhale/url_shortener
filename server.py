from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
import random
import string
import os
import uvicorn


# Loading environment variables from .env file
load_dotenv()

app = FastAPI()

# Loading MongoDB connection string from environment variable
mongo_uri = os.getenv("MONGO_URI")  
client = MongoClient(mongo_uri)
db = client['url_shortener_db']
collection = db['urls']

class URLRequest(BaseModel):
    url: str
    custom_code: Optional[str] = None
    expiration_minutes: Optional[int] = 5  

def generate_short_code(length=6):
    """Generate a random short code of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/url/shorten")
async def shorten_url(request: URLRequest):
    # Using custom code if provided, otherwise generating a new one
    short_code = request.custom_code or generate_short_code()
    
    # Checking for duplicate custom short codes
    if request.custom_code and collection.find_one({"short_code": request.custom_code}):
        raise HTTPException(status_code=400, detail="Custom short code already in use.")
    
    # Ensuring the generated short code is unique
    while collection.find_one({"short_code": short_code}):
        short_code = generate_short_code()
    
    # Setting expiration time if provided
    expiration_time = datetime.utcnow() + timedelta(minutes=request.expiration_minutes) if request.expiration_minutes else None

    # Inserting URL with metadata into MongoDB
    collection.insert_one({
        "short_code": short_code,
        "original_url": request.url,
        "created_at": datetime.utcnow(),
        "expiration_time": expiration_time,
        "access_count": 0
    })
    
    short_url = f"http://localhost:8000/r/{short_code}"
    return {"short_url": short_url}

@app.get("/r/{short_code}")
async def redirect_to_url(short_code: str):
    result = collection.find_one({"short_code": short_code})
    
    # Checking if the URL exists and is not expired
    if not result:
        raise HTTPException(status_code=404, detail="URL not found")
    if result["expiration_time"] and result["expiration_time"] < datetime.utcnow():
        raise HTTPException(status_code=404, detail="URL has expired")
    
    # Updating access count for analytics
    collection.update_one({"short_code": short_code}, {"$inc": {"access_count": 1}})
    
    return RedirectResponse(url=result["original_url"], status_code=302)

# Rate Limiting Middleware
rate_limit = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in rate_limit:
        rate_limit[client_ip] = {"count": 0, "last_request": datetime.utcnow()}
    
    current_time = datetime.utcnow()
    
    # Resetting the count if it's been more than a minute since the last request
    if (current_time - rate_limit[client_ip]["last_request"]).seconds > 60:
        rate_limit[client_ip] = {"count": 1, "last_request": current_time}
    else:
        rate_limit[client_ip]["count"] += 1
    
    # Allowing maximum of 10 requests per minute
    if rate_limit[client_ip]["count"] > 10:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    
    response = await call_next(request)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
