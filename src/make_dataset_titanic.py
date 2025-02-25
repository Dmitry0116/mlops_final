import os
import pandas as pd
from catboost.datasets import titanic

# Путь к директориям с датасетами
DATASETS_PATH = os.path.join("..", "datasets")

# Проверяем, существует ли директория DATASETS_PATH, и создаем её, если нет
if not os.path.exists(DATASETS_PATH):
    try:
        os.makedirs(DATASETS_PATH)
        print(f"The {DATASETS_PATH} Директория создана.")
    except OSError as e:
        print(f"Ошибка при создании директории: {e}")

# Загрузка датасета Titanic
train_df, _ = titanic()
print(train_df.info())

# Сохранение датасета в CSV
csv_file_path = os.path.join(DATASETS_PATH, 'dataset_titanic.csv')
try:
    train_df.to_csv(csv_file_path, index=False)
    print(f"Датасет успешно сохранен в директорию {DATASETS_PATH} под именем dataset_titanic.csv.")
except Exception as e:
    print("Ошибка при сохранении датасета:", e)