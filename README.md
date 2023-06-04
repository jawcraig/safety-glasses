Safety Glasses
====

Safety and debug tools for python programs

see safety_glasses/test.py for examples

Use alarm signal to interrupt hanged system call
----
    from safety_glasses.grafecul_timeout import graceful_timeout
    try:
        with graceful_timeout(5) as result:
            print(result):
            with open('remote-file.txt') as fp:
                result = fp.read()
    except OSError:
        print("interrupted")



Add program global state printer signal
----

```python
# Add global state handler to your importable module:

def safety_debug_global_state():
    """
    Return a triplet:

    name: str,
    states: list(tuple(str, str))
    children: list(str)
    """
    return 'my_fancy_module', [
        ("global_value1", repr(global_value1)),
    ], ['also_check_related_module', 'i_import_something']


# Output global state as toml:
    from safety_glasses.output_global_state import output_global_state
    output_global_state(tomler, stream=sys.stdout)

# Add SIGUSR1 handler for toml output and SIGUSR2 handler for dot output:
    from safety_glasses.output_global_state import setup_global_state_output
    setup_global_state_output()
```

# Send user signal to program
```bash
# Output tomli to logger using signal SIGUSR1
kill -SIGUSR1 2575

# Output DOT to logger using signal SIGUSR2
kill -SIGUSR2 2575

# Get png from dot (requires graphviz)
dot -Tpng test.dot > test.png
```
