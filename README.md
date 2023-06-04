Safety Glasses
====

Safety and debug tools for python programs

see safety_glasses/test.py for examples

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
    output_global_state(tomler, stream=sys.stdout)

# Add SIGUSR1 handler for toml output and SIGUSR2 handler for dot output:
    setup_global_state_output()
```

# Send user signal to program
```bash
kill -SIGUSR2 2575

# Output png from dot
dot -Tpng test.dot > test.png
```