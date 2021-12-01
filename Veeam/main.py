import subprocess
import time
import psutil
import argparse
import pandas
import sys


def plot_stats():
    import matplotlib.pyplot as plt

    stats = pandas.read_csv('stats.csv')

    plt.figure(1)
    plt.title('Stats')
    plt.plot(stats['timestamp'], stats['cpu'], label='CPU, %')
    plt.plot(stats['timestamp'], stats['rss'], label='RSS, MiB')
    plt.plot(stats['timestamp'], stats['vms'], label='VMS, MiB')
    plt.plot(stats['timestamp'], stats['fds'], label='FDS')
    plt.legend()
    plt.xlabel('Time, sec')
    plt.grid(alpha=0.3)
    plt.savefig('stats.png', dpi=600)


def run_process(path_file, interval, time_limit=None):
    stats = {'timestamp': [], 'cpu': [], 'rss': [], 'vms': [], 'fds': []}
    interval_limit = 3  # При interval > interval_limit каждые interval_limit секунд будет проверяться is_running()

    start_time = time.time()
    process = subprocess.Popen(['python3', path_file], close_fds=True)
    p = psutil.Process(pid=process.pid)

    while p.is_running() and p.status() != psutil.STATUS_ZOMBIE:
        tmp_time = round(time.time() - start_time, 2)
        if time_limit and tmp_time > time_limit:
            print('Exceeded maximum execution time process.')
            p.kill()
            break

        try:
            # Время с начала процесса
            stats['timestamp'].append(tmp_time)

            # Загрузка CPU в процентах
            stats['cpu'].append(p.cpu_percent(0.1) / psutil.cpu_count())

            # Потребление памяти в MiB: Resident Set Size и Virtual Memory Size
            stats['rss'].append(p.memory_info().rss / 1024 / 1024)
            stats['vms'].append(p.memory_info().vms / 1024 / 1024)

            # Количество открытых файловых дескрипторов
            if sys.platform == 'linux':
                stats['fds'].append(p.num_fds())
            else:
                stats['fds'].append(p.num_handles())
        except psutil.Error:
            for value in stats.values():
                if len(value) > len(stats['fds']):
                    value.pop()

        if interval <= interval_limit:
            time.sleep(interval - ((time.time() - start_time) % interval))
        else:
            for i in range(int(interval // interval_limit)):
                if p.is_running() and p.status() != psutil.STATUS_ZOMBIE:
                    time.sleep(interval_limit)
                else:
                    break

    pandas.DataFrame(stats).to_csv('stats.csv', index=False)


if __name__ == "__main__":
    if sys.platform != 'win32' and sys.platform != 'linux':
        print('Only for Windows or Linux systems.')
        sys.exit()

    argParser = argparse.ArgumentParser()
    argParser.add_argument('-p', '--path', required=True,
                           help='Path to executable python file (REQUIRED)')
    argParser.add_argument('-i', '--interval', required=True, type=float,
                           help='Statistics collection interval in seconds (REQUIRED)')
    argParser.add_argument('-t', '--time-limit', type=float,
                           help='Maximum execution time of transferred file in seconds')
    args = argParser.parse_args()

    if args.interval <= 0:
        print('Interval must be positive!')
        sys.exit()

    run_process(args.path, args.interval, args.time_limit)
    plot_stats()
