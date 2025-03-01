# Импорт необходимых библиотек
import questionary  # Библиотека для интерактивного взаимодействия с пользователем
import requests  # Библиотека для выполнения HTTP-запросов
import os  # Библиотека для работы с файловой системой

# URL сервера, с которым будет взаимодействовать CLI
SERVER_URL = "http://127.0.0.1:8000"

class CLI:
    """Класс, представляющий командную строку для взаимодействия с сервером."""

    @staticmethod
    def register_user():
        """Регистрирует нового пользователя на сервере."""
        # Запрос имени пользователя и пароля
        username = questionary.text("Введите имя пользователя:").ask()
        password = questionary.password("Введите пароль:").ask()
        
        # Отправка POST-запроса на сервер для регистрации пользователя
        response = requests.post(f"{SERVER_URL}/register/", json={"username": username, "password": password})
        
        # Вывод сообщения об успешной регистрации или ошибки
        print(response.json()["message"] if response.status_code == 200 else response.json()["detail"])

    @staticmethod
    def upload_file():
        """Загружает CSV-файл на сервер для указанного пользователя."""
        # Запрос имени пользователя и пути к файлу
        username = questionary.text("Введите имя пользователя:").ask()
        file_path = questionary.path("Введите путь к CSV файлу:").ask()
        
        # Проверка существования файла
        if not os.path.exists(file_path):
            print("Ошибка: Файл не найден!")
            return
        
        # Открытие файла и отправка его на сервер
        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file, "text/csv")}
            response = requests.post(f"{SERVER_URL}/upload/{username}", files=files)
        
        # Вывод сообщения об успешной загрузке или ошибки
        print(response.json()["message"] if response.status_code == 200 else response.json()["detail"])

    @staticmethod
    def list_users():
        """Выводит список всех зарегистрированных пользователей."""
        # Отправка GET-запроса на сервер для получения списка пользователей
        response = requests.get(f"{SERVER_URL}/users/")
        
        # Вывод списка пользователей или сообщения об ошибке
        if response.status_code == 200:
            print("Зарегистрированные пользователи:")
            for user in response.json()["users"]:
                print(f"- {user}")
        else:
            print("Ошибка при получении списка пользователей.")

    @staticmethod
    def get_user_data():
        """Получает и выводит данные пользователя по его имени."""
        # Запрос имени пользователя
        username = questionary.text("Введите имя пользователя:").ask()
        
        # Отправка GET-запроса на сервер для получения данных пользователя
        response = requests.get(f"{SERVER_URL}/user/{username}")
        
        # Вывод данных пользователя или сообщения об ошибке
        if response.status_code == 200:
            print(f"Данные пользователя {username}:")
            for item in response.json()["data"]:
                print(item)
        else:
            print(response.json()["detail"])

    @staticmethod
    def main():
        """Основной метод, запускающий интерактивное меню CLI."""
        while True:
            # Предложение пользователю выбрать действие
            choice = questionary.select(
                "Выберите действие:",
                choices=[
                    "1. Зарегистрировать пользователя",
                    "2. Загрузить CSV-файл",
                    "3. Посмотреть список пользователей",
                    "4. Посмотреть данные пользователя",
                    "5. Выйти"
                ],
            ).ask()

            # Обработка выбора пользователя
            if choice.startswith("1"):
                CLI.register_user()
            elif choice.startswith("2"):
                CLI.upload_file()
            elif choice.startswith("3"):
                CLI.list_users()
            elif choice.startswith("4"):
                CLI.get_user_data()
            elif choice.startswith("5"):
                break

if __name__ == "__main__":
    # Запуск CLI, если скрипт выполняется напрямую
    CLI.main()
