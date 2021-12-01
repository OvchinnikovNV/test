# Задача 1
## Условия задачи
Написать программу, которая будет запускать процесс и с указанным интервалом времени
собирать о нём следующую статистику:

* Загрузка CPU (в процентах);
* Потребление памяти: Working Set и Private Bytes (для Windows-систем) или
Resident Set Size и Virtual Memory Size (для Linux-систем);
* Количество открытых хендлов (для Windows-систем) или файловых дескрипторов
(для Linux-систем).

Сбор статистики должен осуществляться всё время работы запущенного процесса.
Путь к файлу, который необходимо запустить, и интервал сбора статистики должны
указываться пользователем. Собранную статистику необходимо сохранить на диске.
Представление данных должно в дальнейшем позволять использовать эту статистику
для автоматизированного построения графиков потребления ресурсов.

## Описание решения

В качестве запускаемого процесса ожидается **python** файл. Для примера был создан
файл **my_process.py**.<br>
Путь к файлу, который необходимо запустить, и интервал сбора
статистики указываются в параметрах командой строки при запуске **main.py**.<br>
Собранная статистика сохраняется в текущей директории в файле **stats.scv**.<br>
Также на основе собранной статистики строятся простые графики и сохраняются в файл
**stats.png** в текущей директории.<br>
Для возможности ограничения времени работы запускаемого процесса был добавлен
параметр **time_limit**. 

## main.py help
-p PATH, --path PATH:<br>
Path to executable python file (REQUIRED)<br>
-i INTERVAL, --interval INTERVAL:<br>
Statistics collection interval in seconds (REQUIRED)<br>
-t TIME_LIMIT, --time-limit TIME_LIMIT:<br>
Maximum execution time of transferred file in seconds

## Примеры запуска
* python3 main.py --path my_process.py --interval 1
* python3 main.py -p my_process.py -i 0.1 -t 120

## Результаты выполнения
Пример собранной статистики [stats.csv](https://github.com/OvchinnikovNV/test/blob/main/Veeam/stats.csv)
<br>
Пример графика:<br>
![stats.png](https://github.com/OvchinnikovNV/test/blob/main/Veeam/stats.png)

