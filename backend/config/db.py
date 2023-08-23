from pymongo import MongoClient
import os

url = os.getenv('MONGO')

# Set up MongoDB connection and collection
client = MongoClient(url)
# Create database named wellfound if it doesn't exist already
db = client['wellfound']
# Create collection named users if it doesn't exist already
user = db['users']