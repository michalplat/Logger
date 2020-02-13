import subprocess
import os
import io
import sys
from contextlib import redirect_stdout, contextmanager


class Logger(object):
    def __init__(self, log_file=os.devnull):
        self.terminal = sys.stdout
        self.log_file = log_file
        self.buffer = io.StringIO()

    def write(self, msg):
        self.buffer.write(msg)
        self.terminal.write(msg)

    def save(self):
        """
        consider clearing  buffer after writing to file
        (if one changes 'w' option to 'a') double save will write double file content
        """
        with open(self.log_file, "w") as file:
            file.write(self.buffer.getvalue())

    @property
    def log_file(self):
        return self._log_file

    @log_file.setter
    def log_file(self, file):
        file = os.path.abspath(file)
        log_directory = os.path.split(file)[0]
        if os.path.isdir(log_directory):
            self._log_file = file
        else:
            self._log_file = os.devnull


@contextmanager
def context_logger(logger):
    """try and finally statement defined in @contextmanager is same as __enter__ and __exit__ method in class"""
    try:
        with redirect_stdout(logger):
            yield
    finally:
        logger.save()


def run_subprocess(*args, **kwargs):
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.STDOUT # error are going to stdout, and stdout is piped to our logger.
    with subprocess.Popen(*args, **kwargs) as proc:
        while True:
            output = proc.stdout.readline().decode("utf-8")
            if output == '' and proc.poll() is not None:
                break
            if output:
                print(output)  # prints to our logger
        rc = proc.poll()
    return rc

