````md
# URL Shortener API 🚀

A simple URL shortener service built using **FastAPI** and **MongoDB Atlas**.  
It allows users to shorten long URLs, use custom codes, set expiration time, and track URL usage.

---

## ⚙️ Tech Stack
- Python 3.7+
- FastAPI
- MongoDB Atlas
- PyMongo
- Uvicorn
- python-dotenv

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-project-folder>
````

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install fastapi pymongo uvicorn python-dotenv
```

---

## 🗄️ MongoDB Setup

* Create a MongoDB Atlas account
* Create a cluster
* Create a database: `url_shortener_db`
* Create a collection: `urls`
* Copy your MongoDB connection string and add it in the project

Example connection string:

```
mongodb+srv://Nikhil:Nikhil@urlshortnerdb.bcpa9.mongodb.net/
```

---

## ▶️ Run the Project

Start the FastAPI server:

```bash
uvicorn server:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

## 📌 API Endpoint

### Shorten URL

**Endpoint:**

```
POST /url/shorten
```

**URL:**

```
http://localhost:8000/url/shorten
```

**Request Body:**

```json
{
  "url": "https://www.reevv.com",
  "custom_code": "mycustomcode",
  "expiration_minutes": 5
}
```

---

## ✨ Features

* URL shortening
* Custom short codes
* URL expiration system
* Redirect to original URL
* Click tracking

---

## 🧠 Design Decisions

* MongoDB used for flexible schema and scalability
* Expiration system keeps database clean
* Custom codes improve user experience
* Basic rate limiting added for abuse protection

---

## ⚠️ Notes

* Default expiration time is **5 minutes**
* Rate limiting is basic and can be improved for production use

---

## 🧪 Testing

You can test using:

* Postman
* Thunder Client (VS Code)
* cURL

---

## 🚀 Future Improvements

* Advanced rate limiting
* User authentication
* Analytics dashboard
* Better validation and error handling

```
