import json
from uuid import uuid1
from fastapi import APIRouter, HTTPException
from models.contact import Contact

routes = APIRouter(tags=["API Contacts"], prefix="/api/v1")

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

@routes.get('/contacts', status_code=200)
async def index():
    return fetch_data_file()

@routes.post('/contacts', status_code=201)
async def store(contact: Contact):
    new_contact = {
        "id": str(uuid1()),
        "name": contact.name,
        "phone": contact.phone,
        "addressLine": contact.addressLines
    }
    contacts = fetch_data_file()
    contacts.append(new_contact)
    if add_data_file(contacts) == False:
        raise HTTPException(status_code=400,
            detail="Error saving a new people")
    return {"message": "Contact Saved", "data": new_contact}

@routes.get('/contacts/{contact_id}', status_code=200)
async def show(contact_id: str):
    contact = [contact for contact in fetch_data_file() if contact['id'] == contact_id]
    if len(contact) <= 0:
        raise HTTPException(status_code=404,
            detail=f"Contact with id {contact_id} does not exist!")
    return contact[0]

@routes.patch('/contacts/{contact_id}', status_code=200)
async def update(contact_id: str, contact_to_update: Contact):
    contact = [contact for contact in fetch_data_file() if contact['id'] == contact_id]
    if len(contact) <= 0:
        raise HTTPException(status_code=404,
            detail=f"Contact with id {contact_id} does not exist!")
    new_contact = {
        "id": contact_id,
        "name": contact_to_update.name,
        "phone": contact_to_update.phone,
        "addressLine": contact_to_update.addressLines
    }
    contacts = fetch_data_file()
    contacts.remove(contact[0])
    contacts.append(new_contact)
    if add_data_file(contacts) == False:
        raise HTTPException(status_code=400,
            detail=f"Error updating contact with id: {contact_to_update.id}")
    return {"message": f"Contact with id: {contact_to_update.id} was updated", "data": new_contact}

@routes.delete('/contacts/{contact_id}', status_code=204)
async def destroy(contact_id: str):
    contact = [contact for contact in fetch_data_file() if contact['id'] == contact_id]
    if len(contact) <= 0:
        raise HTTPException(status_code=404,
            detail=f"Contact with id {contact_id} does not exist!")
    contacts = fetch_data_file()
    contacts.remove(contact[0])
    if add_data_file(contacts) == False:
        raise HTTPException(status_code=404,
            detail=f"Error deleting contact with id: {contact_id}")
    return {"message": f"Contact with id: {contact_id} was deleted"}
