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


@contextmanager
def graceful_timeout(timeout=10):
    """
    Set OS ALARM to happen after timeout
    """
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        yield True
    except Exception:
        yield False
    finally:
        try:
            signal.alarm(0)
        except Exception:
            pass
