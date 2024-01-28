from dotenv import load_dotenv
from os import getenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()
mongo_connection = getenv("MONGO_CONNECT")

db_client = AsyncIOMotorClient(mongo_connection)
db = "Inventory"
inv_collection = db_client.db["Main"]


async def fetch_all_items():
    items = await inv_collection.find().to_list(length=100)
    return items

async def fetch_item(item_name: str):
    item = await inv_collection.find_one({"name": (item_name)})
    return item

async def add_item(name: str, description: str, drawing: str, quantity: int, status: str):
    new_item = {
        "name": name,
        "description": description,
        "drawing": drawing,
        "quantity": quantity,
        "status": status
    }
    result = await inv_collection.insert_one(new_item)
    return result.inserted_id

async def update_item(name: str, description: str, drawing: str, quantity: int, status: str):
    await inv_collection.update_one({"name": name}, {"$set": {"description": description, "drawing": drawing, "quantity": quantity, "status": status}})
    return True

async def delete_item(name:str):
    await inv_collection.delete_one({"name": name})
    return True