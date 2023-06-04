import signal
from contextlib import contextmanager


"""
TODO: remember to use os.open WITH os.O_NONBLOCK can help if open or read can wait
(file system access still blocks, hopefully briefly)
"""


def timeout_handler(signum, frame):
    signame = signal.Signals(signum).name
    print(f'Timeout signal {signame} ({signum}) at {frame}')
    raise OSError(f'Timeout in {frame}!')


class graceful_timeout():
    """
    Set OS ALARM to happen after timeout
    Usage:
    with graceful_timeout(timeout=5) as watched:
        if not watched:
            print('Did not set timeout')
        do_things()
    """

    _timeout = 60
    _setup = False

    def __init__(self, timeout):
        if timeout:
            self._timeout = timeout

    def __enter__(self):
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self._timeout)
            self._setup = True
            return True
        except Exception:
            return False

    def __exit__(self, *args, **kwargs):
        try:
            if self._setup:
                signal.alarm(0)
        except Exception:
            pass
