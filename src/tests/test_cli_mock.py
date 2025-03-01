import unittest
from unittest.mock import patch
from server.cli import CLI

class TestCLI(unittest.TestCase):
    @patch("requests.post")
    def test_register_user(self, mock_post):
        """Тестирование регистрации пользователя.

        Проверяет, что метод CLI.register_user корректно отправляет POST-запрос
        на сервер для регистрации пользователя с заданными именем и паролем.
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "User registered successfully"}
        
        with patch("questionary.text") as mock_text, patch("questionary.password") as mock_password:
            mock_text.return_value.ask.return_value = "testuser"
            mock_password.return_value.ask.return_value = "testpass"

            CLI.register_user()
            mock_post.assert_called_once_with("http://127.0.0.1:8000/register/", json={"username": "testuser", "password": "testpass"})
    
    @patch("requests.post")
    def test_upload_file(self, mock_post):
        """Тестирование загрузки файла.

        Проверяет, что метод CLI.upload_file корректно отправляет POST-запрос
        на сервер для загрузки файла, если файл существует.
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "File uploaded successfully"}

        with patch("questionary.text") as mock_text, patch("questionary.path") as mock_path, patch("builtins.open", unittest.mock.mock_open(read_data="name,age\nJohn,30\nJane,25")), patch("os.path.exists") as mock_exists:
            mock_text.return_value.ask.side_effect = ["testuser"]
            mock_path.return_value.ask.return_value = "test.csv"
            mock_exists.return_value = True

            CLI.upload_file()
            mock_post.assert_called()

    @patch("requests.post")
    def test_upload_file_file_not_found(self, mock_post):
        """Тестирование загрузки файла, если файл не найден.

        Проверяет, что метод CLI.upload_file не отправляет POST-запрос на сервер,
        если указанный файл не существует.
        """
        with patch("questionary.text") as mock_text, patch("questionary.path") as mock_path, patch("os.path.exists") as mock_exists:
            mock_text.return_value.ask.side_effect = ["testuser"]
            mock_path.return_value.ask.return_value = "nonexistent.csv"
            mock_exists.return_value = False

            CLI.upload_file()
            mock_post.assert_not_called()

    @patch("requests.get")
    def test_list_users(self, mock_get):
        """Тестирование получения списка пользователей.

        Проверяет, что метод CLI.list_users корректно отправляет GET-запрос
        на сервер для получения списка пользователей.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"users": ["user1", "user2"]}

        CLI.list_users()
        mock_get.assert_called_once_with("http://127.0.0.1:8000/users/")

    @patch("requests.get")
    def test_get_user_data(self, mock_get):
        """Тестирование получения данных пользователя.

        Проверяет, что метод CLI.get_user_data корректно отправляет GET-запрос
        на сервер для получения данных конкретного пользователя.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": [{"name": "John", "age": "30"}]}
        
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = "testuser"
            CLI.get_user_data()
            mock_get.assert_called_once_with("http://127.0.0.1:8000/user/testuser")

if __name__ == "__main__":
    unittest.main()
