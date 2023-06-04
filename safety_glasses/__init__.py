import signal

__author__ = "Janne Tervo"
__copyright__ = "Copyright 2023 Janne Tervo"
__credits__ = []
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Janne Tervo"
__email__ = "jawcraig@gmail.com"
__status__ = "Produciton"

__all__ = [
    'graceful_timeout',
    'output_global_state', 'output_dot_state', 'output_toml_state', 'setup_global_state_output', 'dotter', 'tomler'
]

from .graceful_timeout import graceful_timeout
from .output_global_state import output_global_state, output_dot_state, output_toml_state, setup_global_state_output, dotter, tomler


def safety_debug_global_state():
    """
    Return a triplet:

    name: str,
    states: list(tuple(str, str))
    children: list(str)
    """
    return 'safety_glasses', [
        ("SIGUSR1", repr(signal.getsignal(signal.SIGUSR1))
         if hasattr(signal, 'SIGUSR1') else 'n/a'),
        ("SIGUSR2", repr(signal.getsignal(signal.SIGUSR1))
         if hasattr(signal, 'SIGUSR2') else 'n/a'),
        ("SIGALRM", repr(signal.getsignal(signal.SIGALRM))
         if hasattr(signal, 'SIGALRM') else 'n/a'),
    ], ['signal']
