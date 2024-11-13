from pyrogram import Client, filters
from pymongo import MongoClient
import os

# Environment Variables (Replace with your details or use .env file)
API_ID = 23508921
API_HASH = "70e3ec4bc651ba1c64371003e3c04b6c"
BOT_TOKEN = "7844302765:AAEzk9bfr4vKbqr7ywk1NLnMCwC0VoM8CzQ"
MONGO_URI = "mongodb+srv://biswaranjangiri17:biswaranjangiri17@cluster0.spcdm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ADMINS = [5710180559]  # Admins list
LOG_CHANNEL = -1002389563282  # Channel to log messages
BIN_CHANNEL = -1002459927795  # Channel for file storage and bin

# MongoDB Setup
client = MongoClient(MONGO_URI)
db = client["autofilter_db"]
files_collection = db["files"]

# Initialize Pyrogram Client
app = Client("AutoFilterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Save file information to MongoDB
@app.on_message(filters.document | filters.video | filters.photo)
async def save_file(client, message):
    file_info = {
        "file_id": message.document.file_id if message.document else message.video.file_id,
        "file_name": message.document.file_name if message.document else "video",
        "caption": message.caption,
    }
    files_collection.insert_one(file_info)
    await message.reply("File saved for future filtering!")

# Search for files based on keywords
@app.on_message(filters.command("search") & filters.private)
async def search_file(client, message):
    query = message.text.split(" ", 1)[1]  # Get the search query
    results = files_collection.find({"file_name": {"$regex": query, "$options": "i"}})
    
    if results.count() > 0:
        for result in results:
            await message.reply_document(result["file_id"], caption=result["caption"])
    else:
        await message.reply("No files found matching your query.")

# Start the Bot
app.run()
