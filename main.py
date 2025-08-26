from fastapi import FastAPI, HTTPException
import schemas

app = FastAPI()

database = {
    1: {"id": 1, "title": "Buy groceries", "description": "Milk, Bread, Eggs", "completed": False},
    2: {"id": 2, "title": "Read book", "description": "Finish reading chapter 4", "completed": False},
    3: {"id": 3, "title": "Workout", "description": "30 minutes cardio", "completed": True}
}

@app.get("/")
def getItems():
    return database

@app.post("/")
def addItem(item: schemas.Task):
    if item.id in database:
        raise HTTPException(status_code=400, detail=f"Task with id {item.id} already exists")
    database[item.id] = item.model_dump() # model_dump() converts Pydantic model to dictionary
    return {"message": "Task added successfully", "task": database[item.id]}

@app.put("/{id}")
def updateItem(id: int, item: schemas.Task):
    if id not in database:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    database[id] = item.model_dump() 
    return {"message": "Task updated successfully", "task": database[id]}

@app.delete("/{id}")
def deleteItem(id: int):
    if id not in database:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    deleted_task = database.pop(id)
    return {"message": "Task deleted successfully", "task": deleted_task}