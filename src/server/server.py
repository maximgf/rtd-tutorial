from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import csv

# Инициализация FastAPI приложения
app = FastAPI()

# Модель пользователя с использованием Pydantic
class User(BaseModel):
    username: str
    password: str

# База данных для хранения пользователей и их файлов
users_db = {}
user_files = {}

def parse_csv(csv_string: str) -> List[Dict[str, str]]:
    """Парсит CSV строку и возвращает список словарей.

    Args:
        csv_string (str): Строка в формате CSV.

    Returns:
        List[Dict[str, str]]: Список словарей, где каждый словарь представляет строку CSV.
    """
    data = []
    lines = csv_string.strip().split("\n")
    if not lines:
        return data

    reader = csv.reader(lines)
    header = next(reader)

    for row in reader:
        row_dict = {}
        for col_name, value in zip(header, row):
            row_dict[col_name] = value.strip()
        data.append(row_dict)

    return data

@app.post("/register/")
def register_user(user: User):
    """Регистрирует нового пользователя.

    Args:
        user (User): Модель пользователя, содержащая username и password.

    Raises:
        HTTPException: Если пользователь уже существует.

    Returns:
        dict: Сообщение об успешной регистрации.
    """
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user.password
    user_files[user.username] = []
    return {"message": "User registered successfully"}

@app.post("/upload/{username}")
async def upload_file(username: str, file: UploadFile = File(...)):
    """Загружает CSV файл для указанного пользователя.

    Args:
        username (str): Имя пользователя, для которого загружается файл.
        file (UploadFile): Файл, загружаемый пользователем.

    Raises:
        HTTPException: Если пользователь не найден.

    Returns:
        dict: Сообщение об успешной загрузке файла.
    """
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    contents = await file.read()
    csv_string = contents.decode("utf-8")
    parsed_data = parse_csv(csv_string)
    user_files[username].extend(parsed_data)
    return {"message": "File uploaded successfully"}

@app.get("/users/")
def get_users():
    """Возвращает список всех зарегистрированных пользователей.

    Returns:
        dict: Список имен пользователей.
    """
    return {"users": list(users_db.keys())}

@app.get("/user/{username}")
def get_user_data(username: str):
    """Возвращает данные, загруженные указанным пользователем.

    Args:
        username (str): Имя пользователя.

    Raises:
        HTTPException: Если пользователь не найден.

    Returns:
        dict: Данные, загруженные пользователем.
    """
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user_files.get(username, [])}

@app.get("/data/{username}")
def get_user_data_json(username: str):
    """Возвращает данные, загруженные указанным пользователем, в формате JSON.

    Args:
        username (str): Имя пользователя.

    Raises:
        HTTPException: Если пользователь не найден.

    Returns:
        List[Dict[str, str]]: Данные, загруженные пользователем.
    """
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_files.get(username, [])

if __name__ == "__main__":
    # Запуск FastAPI приложения с использованием Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
