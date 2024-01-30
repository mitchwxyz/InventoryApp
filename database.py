from dotenv import load_dotenv
from os import getenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from models import Item, UpdateItem


load_dotenv()
mongo_connection = getenv("MONGO_CONNECT")

db_client = AsyncIOMotorClient(mongo_connection)
db = "Inventory"
inv_collection = db_client.db["Main"]


async def get_all_items():
    items = await inv_collection.find({}).to_list(length=None)
    return items


async def fetch_inventory_page(page: int, items_per_page: int):
    skip = (page - 1) * items_per_page
    items = await inv_collection.find().skip(skip).limit(items_per_page).to_list(items_per_page)
    return items

async def fetch_item(item_id: str):
    item = await inv_collection.find_one({"_id": ObjectId(item_id)})
    return item

async def search_items(search_term: str, page, items_per_page:int):
    query = {"$or": [{"name": {"$regex": search_term, "$options": "i"}}, 
                     {"description": {"$regex": search_term, "$options": "i"}},
                     {"drawing": {"$regex": search_term, "$options": "i"}}
                    ]
            }
    skip = (page - 1) * items_per_page
    items = await inv_collection.find(query).skip(skip).limit(items_per_page).to_list(items_per_page)
    return items

async def add_item(item: Item):
    result = await inv_collection.insert_one(item.model_dump())
    return result.inserted_id

async def update_item(item_id:str, up_item: UpdateItem):
    await inv_collection.update_one({"_id": ObjectId(item_id)}, {"$set": up_item.model_dump()})
    return True

async def delete_item(item_id:str):
    await inv_collection.delete_one({"_id": ObjectId(item_id)})
    return True

async def insert_multiple_items(items: list[Item]):
    items_dicts = [item.model_dump() for item in items]
    result = await inv_collection.insert_many(items_dicts)
    return [str(id) for id in result.inserted_ids]
