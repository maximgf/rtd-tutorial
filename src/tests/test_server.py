from fastapi.testclient import TestClient
from server.server import app

# Инициализация тестового клиента для FastAPI приложения
client = TestClient(app)

def test_register_user():
    """Тестирование функционала регистрации пользователя."""
    
    # Тест успешной регистрации нового пользователя
    response = client.post(
        "/register/",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

    # Тест попытки регистрации уже существующего пользователя
    response = client.post(
        "/register/",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_get_users():
    """Тестирование получения списка зарегистрированных пользователей."""
    
    # Регистрация тестового пользователя для проверки
    client.post(
        "/register/",
        json={"username": "testuser2", "password": "testpass"}
    )
    
    # Получение списка пользователей и проверка наличия тестового пользователя
    response = client.get("/users/")
    assert response.status_code == 200
    assert "testuser2" in response.json()["users"]

def test_upload_file():
    """Тестирование функционала загрузки файла для пользователя."""
    
    # Регистрация пользователя для тестирования загрузки файла
    client.post(
        "/register/",
        json={"username": "fileuser", "password": "testpass"}
    )

    # Создание тестового CSV файла
    csv_content = "name,age\nJohn,30\nJane,25"
    files = {
        "file": ("test.csv", csv_content, "text/csv")
    }

    # Тест успешной загрузки файла
    response = client.post(
        "/upload/fileuser",
        files=files
    )
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}

    # Тест загрузки файла для несуществующего пользователя
    response = client.post(
        "/upload/nonexistent",
        files=files
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_user_data():
    """Тестирование получения данных пользователя."""
    
    # Регистрация пользователя для тестирования
    client.post(
        "/register/",
        json={"username": "datauser", "password": "testpass"}
    )

    # Загрузка тестовых данных в формате CSV
    csv_content = "name,age\nJohn,30\nJane,25"
    files = {
        "file": ("test.csv", csv_content, "text/csv")
    }
    client.post("/upload/datauser", files=files)

    # Получение данных пользователя и проверка их корректности
    response = client.get("/user/datauser")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 2
    assert data[0]["name"] == "John"
    assert data[0]["age"] == "30"

    # Тест получения данных для несуществующего пользователя
    response = client.get("/user/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_user_data_json():
    """Тестирование получения данных пользователя в формате JSON."""
    
    # Регистрация пользователя для тестирования
    client.post(
        "/register/",
        json={"username": "jsonuser", "password": "testpass"}
    )

    # Загрузка тестовых данных в формате CSV
    csv_content = "name,age\nJohn,30\nJane,25"
    files = {
        "file": ("test.csv", csv_content, "text/csv")
    }
    client.post("/upload/jsonuser", files=files)

    # Получение данных пользователя в формате JSON и проверка их корректности
    response = client.get("/data/jsonuser")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "John"
    assert data[0]["age"] == "30"

    # Тест получения JSON данных для несуществующего пользователя
    response = client.get("/data/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
