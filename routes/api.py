from http.client import HTTPException
import json
from uuid import uuid1
from fastapi import APIRouter
from models.people import People

routes = APIRouter(tags=["API People"], prefix="/api/v1")

def fetch_data_file():
    try:
        with open('./data/data.json', 'r') as data_file:
            peoples = json.load(data_file)
    except FileNotFoundError:
        return HTTPException(status_code=404, detail="File not found")
    finally:
        data_file.close()
        return peoples

def add_data_file(peoples):
    try:
        with open('./data/data.json', 'w') as data_file:
            json.dump(peoples, data_file)
    except FileNotFoundError:
        return HTTPException(status_code=404, detail="File not found")
    finally:
        data_file.close()
        return True

@routes.get('/peoples', status_code=200)
def index():
    return fetch_data_file()

@routes.post('/peoples', status_code=201)
def store(people: People):
    new_people = {
        "id": str(uuid1()),
        "name": people.name,
        "phone": people.phone,
        "addressLine": people.addressLines
    }
    peoples = fetch_data_file()
    peoples.append(new_people)
    return {"message": "People Inserted", "data": new_people} if add_data_file(peoples) else HTTPException(status_code=404, details="Error saving a new people")

@routes.get('/peoples/{people_id}', status_code=200)
def show(people_id: str):
    people = [people for people in fetch_data_file() if people['id'] == people_id]
    return people[0] if len(people) > 0 else HTTPException(status_code=404, details=f"People with id {people_id} does not exist!")

@routes.put('/peoples/{people_id}', status_code=200)
def update(people_to_update: People):
    people = [people for people in fetch_data_file() if people['id'] == people_to_update.id]
    new_people = {
        "id": people_to_update.id,
        "name": people_to_update.name,
        "phone": people_to_update.phone,
        "addressLine": people_to_update.addressLines
    }
    peoples = fetch_data_file()
    peoples.remove(people[0])
    peoples.append(new_people)
    return {"message": f"People with id: {people_to_update.id} was updated", "data": new_people} if add_data_file(peoples) else HTTPException(status_code=404, details=f"Error updating people with id: {people_to_update.id}")

@routes.delete('/peoples/{people_id}', status_code=200)
def destroy(people_id: str):
    people = [people for people in fetch_data_file() if people['id'] == people_id]
    peoples = fetch_data_file()
    peoples.remove(people[0])
    return {"message": f"People with id: {people_id} was deleted"} if add_data_file(peoples) else HTTPException(status_code=404, details=f"Error deleting people with id: {people_id}")