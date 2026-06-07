from fastapi import FastAPI, status, HTTPException
from db.client import db_client
from db.models.person import Person
from db.schema.person import persons_schema, person_schema
from bson import ObjectId

app = FastAPI()


@app.get("/pyapi/persons", response_model=list[Person])
async def persons():
    return persons_schema(db_client.people.find())
  
  
@app.get("/pyapi/persons/{id}")
async def person(id: str):
    return search_person("_id", ObjectId(id))
  
  
@app.delete("/pyapi/persons/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def person(id: str):

    found = db_client.people.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}
      
      
@app.post("/pyapi/persons", response_model=Person, status_code=status.HTTP_201_CREATED)
async def person(person: Person):
    user_dict = dict(person)
    del user_dict["id"]

    id = db_client.people.insert_one(user_dict).inserted_id

    new_person = person_schema(db_client.people.find_one({"_id": id}))

    return Person(**new_person)
  
  
@app.put("/pyapi/persons/{id}", response_model=Person)
async def person(id: str, person: Person):
  
  update_data = person.model_dump(exclude_unset=True)
  
  if not update_data:
    raise HTTPException(status_code=400, detail="No hay datos para actualizar")
  
  db_client.people.update_one(
    {"_id": ObjectId(id)},
    {"$set": update_data})
  
  updated_person = db_client.people.find_one({"_id": ObjectId(id)})

  if not updated_person:
    raise HTTPException(status_code=404, detail="Persona no encontrada")

  return Person(**person_schema(updated_person))

  
def search_person(field: str, key):
    try:
        person = db_client.people.find_one({field: key})
        return Person(**person_schema(person))
    except:
        return {"error": "No se ha encontrado el contacto"}