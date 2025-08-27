from fastapi import FastAPI, HTTPException, Depends
import schemas
import models

from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine) # Create the database if it doesn't exist

# Dependency to get DB session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

database = {
    1: {"id": 1, "title": "Buy groceries", "description": "Milk, Bread, Eggs", "completed": False},
    2: {"id": 2, "title": "Read book", "description": "Finish reading chapter 4", "completed": False},
    3: {"id": 3, "title": "Workout", "description": "30 minutes cardio", "completed": True}
}

# @app.get("/")
# def getItems():
#     return database

# @app.post("/")
# def addItem(item: schemas.Task):
#     if item.id in database:
#         raise HTTPException(status_code=400, detail=f"Task with id {item.id} already exists")
#     database[item.id] = item.model_dump() # model_dump() converts Pydantic model to dictionary
#     return {"message": "Task added successfully", "task": database[item.id]}

# @app.put("/{id}")
# def updateItem(id: int, item: schemas.Task):
#     if id not in database:
#         raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
#     database[id] = item.model_dump() 
#     return {"message": "Task updated successfully", "task": database[id]}

# @app.delete("/{id}")
# def deleteItem(id: int):
#     if id not in database:
#         raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
#     deleted_task = database.pop(id)
#     return {"message": "Task deleted successfully", "task": deleted_task}

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.post("/")
def addItem(item: schemas.Task, session: Session = Depends(get_session)):
    item=models.Item(
        id=item.id,
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    return item

@app.get("/{id}")
def getItem(id: int, session: Session = Depends(get_session)):
    item=session.query(models.Item).get(id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    return item

@app.put("/{id}")
def updateItem(id: int, item: schemas.Task, session: Session = Depends(get_session)):
   itemObj=session.query(models.Item).get(id)
   itemObj.title=item.title
   itemObj.description=item.description
   itemObj.completed=item.completed
   session.commit()
   return itemObj
   
@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    item=session.query(models.Item).get(id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    session.delete(item)
    session.commit()
    return {"message": "Task deleted successfully"}