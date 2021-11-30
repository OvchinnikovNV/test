import subprocess
import time
import psutil
import argparse
import pandas
from sys import platform


def run_process(path_file, interval):
    stats = {'timestamp': [], 'cpu': [], 'rss': [], 'vms': [], 'fds': []}
    interval_limit = 3
    interval = float(interval)

    start_time = time.time()
    process = subprocess.Popen(['python', path_file], close_fds=True)
    p = psutil.Process(pid=process.pid)

    while p.is_running() and p.status() != psutil.STATUS_ZOMBIE:
        tmp_time = round(time.time() - start_time, 2)

        # Время с начала процесса
        stats['timestamp'].append(tmp_time)

        # Загрузка CPU в процентах
        stats['cpu'].append(p.cpu_percent() / psutil.cpu_count())

        # Потребление памяти: Resident Set Size и Virtual Memory Size
        stats['rss'].append(p.memory_info().rss / 1024 / 1024)
        stats['vms'].append(p.memory_info().vms / 1024 / 1024)

        # Количество открытых файловых дескрипторов
        try:
            stats['fds'].append(p.num_fds())
        except psutil.Error as error:
            stats['fds'].append(-1)
            print(error)

        if interval < interval_limit:
            time.sleep(interval - ((time.time() - start_time) % interval))
        else:
            for i in range(int(interval // interval_limit) - 1):
                if p.is_running() and p.status() != psutil.STATUS_ZOMBIE:
                    time.sleep(interval_limit)
                else:
                    break

    pandas.DataFrame(stats).to_csv('stats.csv', index=False)


# +++ 1: Записать на диск
# +++ 2: Ограничить сверху и снизу значение interval
# +++  : Будем проверять в слипе
# 3: Обрабатывать все ошибки!
# 4: Реализовать для Windows
# +++ 5: Программа виснет, если interval большой, а процесс уже закончился
if __name__ == "__main__":
    print(platform)

    argParser = argparse.ArgumentParser()
    argParser.add_argument('-p', '--path')
    argParser.add_argument('-i', '--interval')
    args = argParser.parse_args()

    run_process(args.path, args.interval)
