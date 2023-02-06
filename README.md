Данный скрипт предназначен для проведения регрессионного тестирования на Local и DEV стендах с генерацией удобного 
отчета в браузере.

Для его работы должен быть установлен Python3.10 и пакет allure

Установка:

1. Клонировать проект в любую удобную директорию
2. Скопировать содержимое файла .env.example в .env.
3. В корне проекта создать папку logs

Смена тестового стенда (По умолчанию dev стенд):

1. В консоле ввести echo $ENV - для OS Linux или echo %ENV% - для OS Windows. local - local стенд, dev - develop стенд.
2. В консоле ввести export ENV=local или export ENV=dev - для OS Linux, set ENV=local или set ENV=dev - для OS Windows

Запуск тестов:

1. Установить нужные пакеты и библиотеки командой pip install -r requirements.txt
2. Запустить тесты с помощью команды pytest -s -v tests/ --alluredir=result
3. Формирование отчёта командой allure serve result