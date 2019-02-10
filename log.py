import datetime


class Log:
    @staticmethod
    def get_datetime():
        return datetime.datetime.now().strftime("%m%d %H:%M:%S")

    @staticmethod
    def print(level, message):
        print("[{time}] [{level}] {message}".format(
            time = Log.get_datetime(),
            level = level,
            message = message
        ))

    @staticmethod
    def warning(message):
        Log.print("WARN", message)

    @staticmethod
    def info(message):
        Log.print("INFO", message)

    @staticmethod
    def debug(message):
        Log.print("DEBG", message)

    @staticmethod
    def error(message):
        Log.print("ERRR", message)
