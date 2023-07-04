Данный скрипт предназначен для проведения регрессионного тестирования на Local и DEV стендах с генерацией удобного 
отчета в браузере

Для его работы должен быть установлен Python3.10 и пакет allure

Установка:

1. Клонировать проект в любую удобную директорию
2. Скопировать содержимое файла .env.example в .env
3. Установить нужные пакеты и библиотеки командой pip install -r requirements.txt

Смена тестового стенда (По умолчанию dev стенд):

1. В консоль ввести 'export ENV=local' или 'export ENV=dev' - для Linux и Мac OS, set ENV=local или set ENV=dev - для OS Windows
2. В консоль ввести 'echo $ENV' - для для Linux и Мac OS, 'echo %ENV%' - для OS Windows. local - local стенд, dev - develop стенд
3. pytest -k "not test and not Test" - сколько всего тестов в проекте.

Запуск тестов:

1. Запустить тесты с помощью команды pytest -s -v tests/ --alluredir=result на dev стенде
2. pytest -s -v -m "not dev_stand" tests/ --alluredir=result на локальном стенде
3. Формирование отчёта командой allure serve result