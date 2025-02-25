import sys
import os

# Получаем правильные пути
SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))  # Каталог со скриптами
PROJECT_PATH = os.path.dirname(SCRIPTS_PATH)  # Каталог проекта
src_path = os.path.join(PROJECT_PATH, 'src')
sys.path.append(src_path)

from fastapi.testclient import TestClient
from api_app_titanic import app

client = TestClient(app)

def test_api_app():
    # Подготовка данных для запроса
    payload = {
        "Pclass": 1,
        "Sex": 0,
        "Age": 20.0,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 15,
        "Embarked": 0
    }
    
    # Отправка POST-запроса
    response = client.post("/predict/", json=payload)
    
    # Проверка статуса ответа
    assert response.status_code == 200, f"Ожидаемый код статуса 200, получен {response.status_code}"
    
    # Проверка наличия ключа 'survival_prediction' в ответе
    json_data = response.json()
    assert 'survival_prediction' in json_data, "'survival_prediction' поле отсутствует в ответе JSON"
    
    # Дополнительная проверка: можно добавить проверку значения, если это необходимо
    # assert json_data['survival_prediction'] in [0, 1], "Неверное значение прогноза"

# Запуск теста, если файл выполняется как основной
if __name__ == "__main__":
    test_api_app()
    print("Тест прошел успешно!")
