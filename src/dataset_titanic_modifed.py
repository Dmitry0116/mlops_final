import os
from catboost.datasets import titanic
from collections import Counter

# Путь к директориям с датасетами
DATASETS_PATH = "../datasets/"

# Проверяем, существует ли директория DATASETS_PATH, и создаем её, если нет
if not os.path.exists(DATASETS_PATH):
    try:
        os.makedirs(DATASETS_PATH)
        print(f"The {DATASETS_PATH} директория создана.")
    except OSError as e:
        print(f"Ошибка при создании директории: {e}")

# Загрузка датасета Titanic
train_df, _ = titanic()

# Заполнение пропущенных значений в столбце 'Age' 
train_df['Age'].fillna(0, inplace=True)

# Подсчитываем количество встречаемости каждого значения в столбце 'Embarked'
counter = Counter(train_df['Embarked'].dropna())  # Убираем NaN перед подсчетом
least_common_value = counter.most_common()[-1][0]  # Находим наименее встречаемое значение

# Заменяем пропущенные значения в 'Embarked' на наименее встречаемое значение
train_df['Embarked'].fillna(least_common_value, inplace=True)

# Сохранение модифицированного датасета в CSV
csv_file_path = os.path.join(DATASETS_PATH, 'dataset_titanic.csv')
try:
    train_df.to_csv(csv_file_path, index=False)
    print(f"Измененный файл сохранен в директории {DATASETS_PATH} под именем 'dataset_titanic.csv'.")
except Exception as e:
    print("Ошибка при сохранении:", e)
