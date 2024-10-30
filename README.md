      Setup and Execution Steps
      
Prerequisites:
Python 3.7 or higher
A MongoDB Atlas account (for database hosting)
FastAPI and its dependencies

Clone the Repository:
git clone <your-repo-url>

Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate

Install Packages:
pip install fastapi pymongo uvicorn python-dotenv 


Set Up MongoDB:
Create a MongoDB Atlas account
Set up a cluster and create a database named "url_shortener_db" with Collection named "urls"
Update the MongoDB connection string in the code with your credentials


My Connection String:
"mongodb+srv://Nikhil:Nikhil@urlshortnerdb.bcpa9.mongodb.net/"

Credentials:
username "Nikhil"
password "Nikhil"

      Running the Application

To start the FastAPI server, run:
uvicorn server:app --reload

            Design Decisions and Trade-offs
            
MongoDB for Storage: I chose MongoDB for its flexibility in handling dynamic data and its scalability to accommodate future growth.

Expiration Mechanism: I implemented an expiration feature to allow URLs to expire after a defined period, ensuring that the database remains clutter-free and only stores relevant data.

Custom Code Option: Users can specify a custom short code, enhancing the user experience by allowing memorable links.

Basic Rate Limiting: A simple middleware is in place to manage the number of requests from individual clients, helping to prevent abuse.

            Implemented Features
            
URL Shortening: Users can convert long URLs into shorter ones.

Redirection: Users can access the original URLs through the shortened links.

Custom Short Codes: Users can provide a custom code for their shortened URL.

Expiration Time: Users can set a duration for how long the shortened URL should be valid.

Access Count Tracking: The service keeps track of how many times each shortened URL has been accessed.

            Deviations from Original Requirements
            
I set a default expiration time of 5 minutes if the user does not provide one.

Rate limiting is currently basic and may require further enhancement based on traffic patterns.

            Testing Instructions
            
You can test the API using tools like Postman

            POST Request
            
Endpoint: http://localhost:8000/url/shorten
Method: POST
Body(Json):
{
"url": "https://www.reevv.com",
"custom_code": "mycustomcode",  
 "expiration_minutes": 5
}
