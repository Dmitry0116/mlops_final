import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, r2_score
import pickle

# Получаем пути к директориям
SCRIPTS_PATH = os.path.dirname(os.path.abspath(__file__))  # Каталог со скриптами
PROJECT_PATH = os.path.dirname(SCRIPTS_PATH)               # Каталог проекта

# Пути к датасетам и моделям
DATASETS_PATH = os.path.join(PROJECT_PATH, "datasets")

# Загрузка датасета Titanic из файла CSV
train_df = pd.read_csv(os.path.join(DATASETS_PATH, 'dataset_titanic.csv'))

# Заполнение пропущенных значений
train_df['Age'].fillna(train_df['Age'].median(), inplace=True)
train_df['Embarked'].fillna(train_df['Embarked'].mode()[0], inplace=True)

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
print(f"Accuracy: {accuracy:.4f}")
r2 = r2_score(y_test, y_pred)
print(f"Коэффициент детерминации: {r2:.4f}")

print('Classification Report:')
print(classification_report(y_test, y_pred))

# Проверка и создание директории для модели
model_path = os.path.join(PROJECT_PATH, "models")
os.makedirs(model_path, exist_ok=True)  # Создание директории, если она не существует

# Сохранение модели
model_file_path = os.path.join(model_path, 'model_titanic.pkl')
with open(model_file_path, 'wb') as file:
    pickle.dump(rf_model, file)
    print(f'Модель успешно сохранена: {model_file_path}')
