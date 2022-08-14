import json
from typing import List, Union
from uuid import uuid1
from fastapi import APIRouter, HTTPException
from models.contact import Contact
from config.database import create_connection

routes = APIRouter(tags=["API Contacts"])

def fetch_data_file():
    try:
        with open('./data/data.json', 'r') as data_file:
            contacts = json.load(data_file)
    except FileNotFoundError:
        return HTTPException(status_code=500, detail="File not found")
    except json.JSONDecodeError:
        return HTTPException(status_code=500, detail="Error at read the file")
    finally:
        data_file.close()
        return contacts

def add_data_file(peoples):
    try:
        with open('./data/data.json', 'w') as data_file:
            json.dump(peoples, data_file)
    except FileNotFoundError:
        return HTTPException(status_code=500, detail="File not found")
    except json.JSONDecodeError:
        return HTTPException(status_code=500, detail="Error at read the file")
    finally:
        data_file.close()
        return True

@routes.get('/contacts', status_code=200, response_model=List[Contact])
async def index(phrase: Union[str, None] = None):
    contacts = create_connection()["contacts"].find()
    contacts = sorted(contacts, key=lambda contact: contact['name'], reverse=False)
    if phrase:
        contacts = list(filter(lambda contact: contact['name'].lower().__contains__(phrase.lower()), contacts))
    elif phrase == '':
        raise HTTPException(status_code=400, detail='Phrase is empty')
    return contacts

@routes.post('/contacts', status_code=201)
async def store(contact: Contact):
    contact.id = str(contact.id)
    new_contact = create_connection()["contacts"].insert_one(dict(contact))
    contact_found = create_connection()["contacts"].find_one({'_id': new_contact.inserted_id})
    if contact_found:
        return {"message": "Contact Saved", "data": contact}
    else:
        raise HTTPException(status_code=400, detail="Error saving a new contact")

@routes.get('/contacts/{contact_id}', status_code=200)
async def show(contact_id: str):
    contact = create_connection()["contacts"].find_one({'id': contact_id}, {'_id': 0})
    if contact == None:
        raise HTTPException(status_code=404,
            detail=f"Contact with id {contact_id} does not exist!")
    return contact

@routes.patch('/contacts/{contact_id}', status_code=200)
async def update(contact_id: str, contact_to_update: Contact):
    contact = create_connection()["contacts"].find_one({'id': contact_id}, {'_id': 0})
    if contact == None:
        raise HTTPException(status_code=404,
            detail=f"Contact with id {contact_id} does not exist!")
    contact_to_update.id = contact_id
    contact_updated = create_connection()["contacts"].find_one_and_update({"id": contact_id},
        { "$set":dict(contact_to_update)}, {'_id': 0})
    print(contact_updated)
    if contact_to_update:
        return {"message": f"Contact with id: {contact_to_update.id} was updated", "data": contact_updated}
    else:
        raise HTTPException(status_code=400,
            detail=f"Error updating contact with id: {contact_to_update.id}")

@routes.delete('/contacts/{contact_id}', status_code=204)
async def destroy(contact_id: str):
    contact = create_connection()["contacts"].find_one({'id': contact_id}, {'_id': 0})
    if contact == None:
        raise HTTPException(status_code=404,
            detail=f"Contact with id {contact_id} does not exist!")
    create_connection()["contacts"].find_one_and_delete({'id': contact_id}, {'_id': 0})
    contact_exists = create_connection()["contacts"].find_one({'id': contact_id})
    if contact_exists == None:
        return {"message": f"Contact with id: {contact_id} was deleted"}
    else:
        raise HTTPException(status_code=404,
            detail=f"Error deleting contact with id: {contact_id}")