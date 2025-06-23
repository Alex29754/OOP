from typing import Protocol, List
import re, socket

# region Protocols
class LogFilterProtocol(Protocol):
    def match(self, text: str) -> bool: ...


class LogHandlerProtocol(Protocol):
    def handle(self, text: str) -> None: ...
# endregion

# region Filters
class SimpleLogFilter:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, text: str) -> bool:
        return self.pattern in text


class ReLogFilter:
    def __init__(self, pattern: str):
        try:
            self.pattern = re.compile(pattern)
        except re.error as e:
            print(f"\033[91m[REGEX ERROR] Invalid regex pattern: {e}\033[0m")
            self.pattern = None

    def match(self, text: str) -> bool:
        try:
            if self.pattern is None:
                return False
            return bool(self.pattern.search(text))
        except Exception as e:
            print(f"\033[91m[REGEX MATCH ERROR] Failed to apply regex: {e}\033[0m")
            return False
# endregion

# region Handlers
class ConsoleHandler:
    def handle(self, text: str) -> None:
        print(text)


class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename

    def handle(self, text: str) -> None:
        try:
            with open(self.filename, 'a') as f:
                f.write(text + '\n')
        except Exception as e:
            print(f"\033[91m[FILE ERROR] Failed to write to file: {e}\033[0m")


class SocketHandler:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def handle(self, text: str) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall((text + '\n').encode('utf-8'))
        except Exception as e:
            print(f"\033[91m[SOCKET ERROR] Failed to send log: {e}\033[0m")


class SyslogHandler:
    def handle(self, text: str) -> None:
        print(f"\033[93m[SYSLOG] {text}\033[0m")
# endregion

# region Logger
class Logger:
    def __init__(self, filters: List[LogFilterProtocol] = None, handlers: List[LogHandlerProtocol] = None):
        self.filters = filters if filters else []
        self.handlers = handlers if handlers else []

    def log(self, text: str) -> None:
        if self.filters and not any(f.match(text) for f in self.filters):
            return

        for handler in self.handlers:
            handler.handle(text)
# endregion

# region Demonstration
if __name__ == "__main__":
    errorFilter = SimpleLogFilter("ERROR")
    warningFilter = SimpleLogFilter("WARNING")
    httpFilter = ReLogFilter(r"HTTP/\d\.\d")

    consoleHandler = ConsoleHandler()
    fileHandler = FileHandler("Log.log")
    socketHandler = SocketHandler("localhost", 6969)  # фейковый адрес
    syslogHandler = SyslogHandler()

    errorLogger = Logger(filters=[errorFilter], handlers=[consoleHandler, fileHandler, syslogHandler])
    warningLogger = Logger(filters=[warningFilter], handlers=[consoleHandler, fileHandler])
    httpLogger = Logger(filters=[httpFilter], handlers=[consoleHandler, fileHandler, socketHandler])
    defaultLogger = Logger(handlers=[consoleHandler])

    testLogs = [
        "INFO: Today is a good day",
        "ERROR: Application is not responding",
        "WARNING: Memory leakage",
        "INFO: HTTP/1.1 request received",
        "ERROR: HTTP/2.0 connection error"
    ]

    print("ERROR logs:")
    for logText in testLogs:
        errorLogger.log(logText)

    print("---------------\nWARNING logs:")
    for logText in testLogs:
        warningLogger.log(logText)

    print("---------------\nHTTP logs:")
    for logText in testLogs:
        httpLogger.log(logText)

    print("---------------\nALL logs:")
    for logText in testLogs:
        defaultLogger.log(logText)
# endregion
