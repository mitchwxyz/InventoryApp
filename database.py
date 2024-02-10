from dotenv import load_dotenv
from os import getenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from models import Item, UpdateItem


load_dotenv()
mongo_connection = getenv("MONGO_CONNECT")

db_client = AsyncIOMotorClient(mongo_connection)
inv_collection = db_client.InventoryApp["Item"]


async def get_all_items(user_id: str):
    """
    Retrieve all items from the inventory collection.

    This function asynchronously fetches all the documents (items) from the 'Main' collection
    of the 'Inventory' database in MongoDB.

    Returns:
        list: A list of dictionaries, where each dictionary represents an item from the inventory.
    """
    items = await inv_collection.find({"user_id": user_id}).to_list(length=None)
    return items


async def fetch_inventory_page(page: int, items_per_page: int, user_id: str):
    """
    Fetch a specific page of items from the inventory collection.

    This function performs pagination by skipping a certain number of documents and then
    limiting the query to a specified number of items per page.

    Args:
        page (int): The page number to fetch.
        items_per_page (int): The number of items per page.

    Returns:
        list: A list of dictionaries, each representing an item for the specified page.
    """
    skip = (page - 1) * items_per_page
    items = await inv_collection.find({"user_id": user_id}).skip(skip).limit(items_per_page).to_list(items_per_page)
    return items


async def fetch_item(item_id: str):
    """
    Fetch a single item from the inventory collection using its ID.

    Args:
        item_id (str): The unique identifier of the item to fetch.

    Returns:
        dict: A dictionary representing the fetched item, or None if the item is not found.
    """
    item = await inv_collection.find_one({"_id": ObjectId(item_id)})
    return item


async def search_items(search_term: str, page, items_per_page:int, user_id: str):
    """
    Search for items in the inventory collection matching a search term.

    This function supports pagination and searches for items based on their name, description,
    or drawing fields.

    Args:
        search_term (str): The term to search within the items.
        page (int): The page number of the search results to fetch.
        items_per_page (int): The number of items per page in the search results.

    Returns:
        list: A list of dictionaries, each representing an item that matches the search term.
    """
    query = {"$and": [
                    {"$or": [{"name": {"$regex": search_term, "$options": "i"}}, 
                     {"description": {"$regex": search_term, "$options": "i"}},
                     {"drawing": {"$regex": search_term, "$options": "i"}}
                    ]},
                    {"user_id": user_id}
                    ]}   
    skip = (page - 1) * items_per_page
    items = await inv_collection.find(query).skip(skip).limit(items_per_page).to_list(items_per_page)
    return items


async def add_item(item: Item):
    """
    Add a new item to the inventory collection.

    Args:
        item (Item): An instance of the Item class representing the item to be added.

    Returns:
        str: The unique identifier of the newly inserted item.
    """
    result = await inv_collection.insert_one(item.model_dump())
    return result.inserted_id


async def update_item(item_id:str, up_item: UpdateItem):
    """
    Update an existing item in the inventory collection.

    Args:
        item_id (str): The unique identifier of the item to update.
        up_item (UpdateItem): An instance of the UpdateItem class containing the updated values.

    Returns:
        bool: True if the update operation was successful, False otherwise.
    """
    await inv_collection.update_one({"_id": ObjectId(item_id)}, {"$set": up_item.model_dump()})
    return True


async def delete_item(item_id:str):
    """
    Delete an item from the inventory collection.

    Args:
        item_id (str): The unique identifier of the item to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    await inv_collection.delete_one({"_id": ObjectId(item_id)})
    return True


async def insert_multiple_items(items: list[Item]):
    """
    Insert multiple items into the inventory collection.

    Args:
        items (list[Item]): A list of Item instances representing the items to be added.

    Returns:
        list: A list of string identifiers for the newly inserted items.
    """
    items_dicts = [item.model_dump() for item in items]
    result = await inv_collection.insert_many(items_dicts)
    return [str(id) for id in result.inserted_ids]


async def cleanup_old_records(age):
    await inv_collection.delete_many({"update_date": {"$lt": age}})
