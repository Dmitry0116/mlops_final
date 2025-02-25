# Используем официальный образ Python версии 3.10
FROM python:3.10-slim

# Обновляем список пакетов и устанавливаем curl (если необходимо для вашего приложения)
# RUN apt-get update && apt-get install -y curl

# Устанавливаем рабочий каталог приложения в контейнере
WORKDIR /usr/src/app

# Копируем файл requirements.txt в рабочий каталог
COPY requirements.txt ./

# Устанавливаем необходимые модули для Python из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код приложения в контейнер
COPY . .

# Запускаем приложение с помощью Uvicorn
CMD ["uvicorn", "src.api_app_titanic:app", "--host", "0.0.0.0", "--port", "8091"]
