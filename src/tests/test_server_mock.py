import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from server.server import app

# Инициализация тестового клиента для FastAPI приложения
client = TestClient(app)

class TestServer(unittest.TestCase):
    @patch("server.server.users_db", {})
    @patch("server.server.user_files", {})
    def test_register_user(self):
        """Тестирование регистрации нового пользователя.
        
        Проверяет, что при отправке POST-запроса на эндпоинт /register/ 
        с корректными данными, возвращается статус код 200 и сообщение об успешной регистрации.
        """
        response = client.post("/register/", json={"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User registered successfully"})

    @patch("server.server.users_db", {"testuser": "testpass"})
    @patch("server.server.user_files", {"testuser": []})
    def test_upload_file(self):
        """Тестирование загрузки файла для пользователя.
        
        Проверяет, что при отправке POST-запроса на эндпоинт /upload/{username} 
        с корректным файлом, возвращается статус код 200 и сообщение об успешной загрузке файла.
        """
        csv_content = "name,age\nJohn,30\nJane,25"
        files = {"file": ("test.csv", csv_content, "text/csv")}
        response = client.post("/upload/testuser", files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "File uploaded successfully"})

    @patch("server.server.users_db", {"testuser": "testpass"})
    def test_get_users(self):
        """Тестирование получения списка зарегистрированных пользователей.
        
        Проверяет, что при отправке GET-запроса на эндпоинт /users/ 
        возвращается статус код 200 и список пользователей, содержащий тестового пользователя.
        """
        response = client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("testuser", response.json()["users"])

    @patch("server.server.users_db", {"testuser": "testpass"})
    @patch("server.server.user_files", {"testuser": [{"name": "John", "age": "30"}]})
    def test_get_user_data(self):
        """Тестирование получения данных пользователя.
        
        Проверяет, что при отправке GET-запроса на эндпоинт /user/{username} 
        возвращается статус код 200 и данные пользователя.
        """
        response = client.get("/user/testuser")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": [{"name": "John", "age": "30"}]})

    @patch("server.server.users_db", {"testuser": "testpass"})
    @patch("server.server.user_files", {"testuser": [{"name": "John", "age": "30"}]})
    def test_get_user_data_json(self):
        """Тестирование получения данных пользователя в формате JSON.
        
        Проверяет, что при отправке GET-запроса на эндпоинт /data/{username} 
        возвращается статус код 200 и данные пользователя в формате JSON.
        """
        response = client.get("/data/testuser")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"name": "John", "age": "30"}])

if __name__ == "__main__":
    # Запуск всех тестов, если скрипт выполняется напрямую
    unittest.main()
