import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, r2_score
import pickle

# Получаем правильные пути
SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))  # Каталог со скриптами
PROJECT_PATH = os.path.dirname(SCRIPTS_PATH)  # Каталог проекта

# Путь к датасетам
DATASETS_PATH = os.path.join(PROJECT_PATH, "datasets")

# Загрузка датасета Titanic из файла CSV
try:
    train_df = pd.read_csv(os.path.join(DATASETS_PATH, 'dataset_titanic.csv'))
except FileNotFoundError:
    print("Файл dataset_titanic.csv не найден. Проверьте путь к файлу.")
    exit()

# Заполнение пропущенных значений
train_df['Age'] = train_df['Age'].fillna(train_df['Age'].median())
train_df['Embarked'] = train_df['Embarked'].fillna(train_df['Embarked'].mode()[0])

# Преобразование категориальных признаков
label_encoders = {}
for col in ['Sex', 'Embarked']:
    le = LabelEncoder()
    train_df[col] = le.fit_transform(train_df[col])
    label_encoders[col] = le

# Разделение данных на признаки и целевую переменную
X = train_df.drop(['PassengerId', 'Survived', 'Name', 'Ticket', 'Cabin'], axis=1)
y = train_df['Survived']

# Разделение на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели случайного леса
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Предсказание на тестовом наборе
y_pred = rf_model.predict(X_test)

# Оценка качества модели
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность: {accuracy:.2f}")
r2 = r2_score(y_test, y_pred)
print(f"Коэффициент детерминации: {r2:.2f}")

# Сохранение модели в файл
def save_model(model, filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

# Загрузка модели из файла
def load_model(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# Сохранение модели
save_model(rf_model, os.path.join(PROJECT_PATH, 'rf_model.pkl'))

# Функция тестирования предсказаний
def test_predictions():
    assert r2_score(y_test, y_pred) > 0.2, "Проблема с датасетом"
    print("Тестирование прошло успешно!")

# Запуск тестирования
test_predictions()
