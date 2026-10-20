from datetime import datetime


class Logger:
    """Log error and status info to a file or the terminal."""

    def __init__(self, log_file: str = None, to_terminal: bool = True):
        self.log_file = log_file
        self.to_terminal = to_terminal

    # inject a file for writing log messages
    def register_log_file(self, file_name: str):
        """Register a file for log data to be written to. Optional."""
        try:
            self.log_file = open(file_name, 'a')
        except Exception as e:
            print(f"Unable to load logfile {file_name}:", e)

    def _log_event(self, message, event_type):
        stamped_message = f"[{datetime.now()}] [{event_type}] {message}\n"

        if self.log_file:
            self.log_file.write(stamped_message)
        if self.to_terminal:
            # TODO: more formatting / colors / etc?
            print(stamped_message, end="")  # string comes with newline
        return stamped_message

    def info(self, message):
        """Log the given informational message with a formatted timestamp."""
        return self._log_event(message, "INFO")

    def error(self, message):
        """Log the given error message with a formatted timestamp."""
        return self._log_event(message, "ERROR")

    def warning(self, message):
        """Log the given warning message with a formatted timestamp."""
        return self._log_event(message, "WARN")

    # log an incoming request
    def incoming(self, req):
        """Log incoming request info."""
        message = (f"Incoming -> Method: [{req.method}]"
                   f" - URL: [{req.url}] - IP: [{req.remote_addr}]"
                   )
        return self.info(message)

    # log request result(s)
    def result(self, req, res):
        """Log outgoing response status."""
        message = (f"Result   -> Method: [{req.method}]"
                   f" - URL: [{req.url}] - IP: [{req.remote_addr}]"
                   f" - Status: [{res.status}]"
                   )
        return self.info(message)

    # # log an event?
    # def event(self, e, message=None):
    #     pass


Log = Logger()
