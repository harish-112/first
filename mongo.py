from pymongo import MongoClient

# Connect to MongoDB (Update with your credentials)
client = MongoClient("mongodb://localhost:27017/")  
db = client["sentiment_analysis"]
collection = db["product_sentiment"]

# Function to save results
def save_to_mongo(product, sentiment_data, recommendation):
    records = sentiment_data.to_dict(orient="records")
    collection.insert_one({
        "product": product,
        "sentiment_data": records,
        "recommendation": recommendation
    })
    print("✅ Data saved to MongoDB!")
print(hii)