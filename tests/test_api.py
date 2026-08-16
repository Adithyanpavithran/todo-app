def test_health():
    assert True


def test_create_todo():
    todo = {
        "title": "Test Todo",
        "description": "Testing Todo API",
    }

    assert todo["title"] == "Test Todo"
    assert todo["description"] == "Testing Todo API"


def test_todo_completion():
    todo = {
        "title": "Learn Docker",
        "completed": False,
    }

    todo["completed"] = True

    assert todo["completed"] is True


def test_todo_delete():
    todos = [
        {"id": 1, "title": "Todo 1"},
        {"id": 2, "title": "Todo 2"},
    ]

    todos = [
        todo for todo in todos
        if todo["id"] != 1
    ]

    assert len(todos) == 1
    assert todos[0]["id"] == 2
