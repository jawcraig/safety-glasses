#!/usr/bin/env python

import sys
import time
from safety_glasses import output_global_state, tomler, dotter, setup_global_state_output, graceful_timeout


def main():
    """
    Example usage:
    """
    output_global_state(tomler, stream=sys.stdout)
    # output_global_state(dotter, stream=sys.stdout)

    setup_global_state_output()

    with graceful_timeout(10) as is_handled:
        print(f'{is_handled=}')
        # output_global_state(tomler, stream=sys.stdout)
        output_global_state(dotter, stream=sys.stdout)
        time.sleep(1)

    print('OK up to here, now break:')

    try:
        with graceful_timeout(30) as is_handled:
            print(f'{is_handled=}')
            time.sleep(600)
    except OSError as e:
        print('YES, GOT ' + str(e))
    else:
        print('SHOULD NOT GET HERE')



if __name__ == '__main__':
    main()
