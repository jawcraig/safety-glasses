import signal
import sys
import threading
import traceback
from datetime import datetime


def get_stack_trace():
    trace = ""

    for thread in threading.enumerate():
        trace += str(thread)
        stack = traceback.format_stack(sys._current_frames()[thread.ident])
        trace += "".join(stack)

    return trace


def dot_header():
    return """\
digraph G {
    fontname = "Consolas"
    fontsize = 8
    node [
        fontname = "Consolas"
        fontsize = 8
        shape = "record"
    ]
    edge [
        fontname = "Consolas"
        fontsize = 8
    ]

    """


def dot_state(module, properties, children):
    module_title = module.capitalize()
    states = '|'.join([f'+ {state}: {repr(value).replace("<", "&lt;").replace(">", "&gt;")}\l' for state,
                      value in properties]) if properties else '???'
    child_list = '\n'.join(
        [f'{module_title}->{child.capitalize()}' for child in children]) if children else ''
    return f"""
{module_title} [
    label = "{{{module}|{states}}}"
]

{child_list}

"""


def dot_footer():
    return """
}
"""


def dotter(states):
    yield dot_header()
    for state in states:
        try:
            yield dot_state(*state)
        except Exception as e:
            print(f'***ERROR: {e}')
    yield dot_footer()


def toml_header():
    trace = get_stack_trace()
    return f"""\
time={datetime.utcnow().isoformat()}
stack='''{trace}'''

"""


def toml_state(module, states, children):
    child_list = 'children=[' + \
        ('"' + "', '".join(children) + '"]') if children else ']'
    # TODO: Output states as TOML types 
    state_list = '\n'.join(
        [f"{state}={repr(value)}" for state, value in states])
    return f"""\
[{module}]
{state_list}
{child_list}

"""


def toml_footer():
    return """
"""


def tomler(states):
    yield toml_header()
    for state in states:
        try:
            yield toml_state(*state)
        except Exception as e:
            print(f'***ERROR: {e}')
    yield toml_footer()


def get_global_state():
    for module in sys.modules.values():
        if hasattr(module, 'safety_debug_global_state'):
            yield getattr(module, 'safety_debug_global_state')()


def output_global_state(handler, stream):
    states = list(get_global_state())
    for result in handler(states):
        stream.write(result)


def output_toml_state(*args, **kwargs):
    output_global_state(tomler, stream=sys.stdout)


def output_dot_state(*args, **kwargs):
    output_global_state(dotter, stream=sys.stdout)


def setup_global_state_output():
    if 'safety_glasses' not in sys.modules:
        sys.stderr.write(
            'safety_glasses not in sys.modules, now why would that be?')

    if hasattr(signal, 'SIGUSR1'):
        signal.signal(signal.SIGUSR1, output_toml_state)
    else:
        sys.stderr.write('no signal.SIGUSR1, are we running on a potato?\n')

    if hasattr(signal, 'SIGUSR2'):
        signal.signal(signal.SIGUSR2, output_dot_state)
    else:
        sys.stderr.write('no signal.SIGUSR2, are we running on a potato?\n')
