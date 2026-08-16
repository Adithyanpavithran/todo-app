from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "todo-api",
    }


@app.get("/todos", response_model=list[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
        )

    return todo


@app.post(
    "/todos",
    response_model=schemas.TodoResponse,
    status_code=201,
)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
):
    new_todo = models.Todo(
        title=todo.title,
        description=todo.description,
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@app.put(
    "/todos/{todo_id}",
    response_model=schemas.TodoResponse,
)
def update_todo(
    todo_id: int,
    todo_data: schemas.TodoUpdate,
    db: Session = Depends(get_db),
):
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
        )

    update_data = todo_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)

    return todo


@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
        )

    db.delete(todo)
    db.commit()

    return {
        "message": "Todo deleted successfully"
    }
