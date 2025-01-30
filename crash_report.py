# crash_report.py
import traceback
import datetime

def log_crash(error_message):
    """
    Записывает информацию об ошибке в файл crash_report.txt.
    :param error_message: Сообщение об ошибке или трассировка стека.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("crash_report.txt", "a") as file:
        file.write(f"--- Crash Report ---\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Error: {error_message}\n")
        file.write("-" * 30 + "\n")