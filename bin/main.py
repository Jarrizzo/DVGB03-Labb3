#!/usr/bin/env python3

import os
import sys
import logging
import argparse

current_path = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_path, "../src"))
sys.path.insert(0, src_path)

log = logging.getLogger(__name__)

from ui import TerminalUI

def main(args):
    try:
        logging.basicConfig(
            format="[%(levelname)s] %(message)s",
            level = logging.__dict__[args.log_level.upper()],
        )
    except KeyError:
        log.critical("invalid log level: {}".format(args.log_level))
        return 1

    try:
        mode = args.mode
        return TerminalUI(mode if mode == "undirected" else "directed",
                          args.echo).run()
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass

def get_args():
    parser = argparse.ArgumentParser("Terminal-based UI - (un)directed graphs")
    parser.add_argument("--log-level", "-l", type=str, default="info",
        help="Minimum verbosity for logging.  Available in ascending order: "
        "debug, info, warning, error, crirical.",
    )
    parser.add_argument("--mode", "-m", type=str, default="directed",
        help="Graph mode.  Available options: undirected, directed.",
    )
    parser.add_argument("--echo", "-e", action="store_true",
        help="Echo input. Useful if redirecting input from file"
    )
    return parser.parse_args()

if __name__ == "__main__":
    sys.exit(main(get_args()))
