import os
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd

# Получаем правильные пути
SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))      # Каталог со скриптами
PROJECT_PATH = os.path.dirname(SCRIPTS_PATH)                   # Каталог проекта

# Загрузим модель из файла pickle
model_path = os.path.join(PROJECT_PATH, 'models', 'model_titanic.pkl')
try:
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
        print("The model has been successfully loaded.")
except FileNotFoundError:
    print(f"Файл модели не найден {model_path}. Пожалуйста укажите путь.")
    raise
except Exception as e:
    print(f"Ошибка при загрузке модели: {e}")
    raise

# Определение класса для данных о пассажире
class Passenger(BaseModel):
    Pclass: int         # Класс: 1, 2, 3
    Sex: float          # Пол: 0, 1
    Age: float          # Возраст
    SibSp: int          # Количество родственников (супруг+братья/сестры): 0, 1, 2, 3
    Parch: int          # Количество родственников (родители+дети): 0, 1, 2
    Fare: float         # Стоимость билета
    Embarked: float     # Порт отправления

app = FastAPI()

@app.post("/predict")
async def predict_survival(passenger: Passenger):
    # Преобразуем данные о пассажире в массив NumPy
    test_data = np.array([[passenger.Pclass, passenger.Sex, passenger.Age,
                           passenger.SibSp, passenger.Parch, passenger.Fare, passenger.Embarked]])

    # Устанавливаем имена признаков для DataFrame
    column_names = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    X_test = pd.DataFrame(test_data, columns=column_names)

    # Делаем предсказание
    try:
        prediction = model.predict(X_test)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при прогнозировании: {e}")

    return {"survival_prediction": int(prediction[0])}

# Запуск FastAPI приложения
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8091)
