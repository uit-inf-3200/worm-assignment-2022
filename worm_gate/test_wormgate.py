#!/usr/bin/env python3

import argparse
import logging
import os
import re
import subprocess
import tempfile
import time
import unittest
import wormgate

#logging.basicConfig(level=logging.INFO)

opts_to_pipe_output = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
        }

# Simple bash worms
#=================================================================

hello_worm = """
#!/bin/bash
echo "Hello, World!"
""".strip().encode("utf-8")

show_args_reverse = """
#!/bin/bash
echo "$3 $2 $1"
""".strip().encode("utf-8")

continuous_echo = """
#!/bin/bash
echo "Starting loop"
while true; do
    sleep .05
    echo "Child process running"
done
""".strip().encode("utf-8")

# Tests
#=================================================================

class TestWormProcess(unittest.TestCase):

    def test_start(self):
        script = hello_worm

        proc = wormgate.WormProcess(script, popen_kwargs=opts_to_pipe_output)

        try:
            (output, _) = proc.popen.communicate()
            self.assertEqual(output, b"Hello, World!\n")

        finally:
            proc.cleanup()

        self.assertFalse(os.path.exists(proc.execfile.name))


    def test_args(self):
        script = show_args_reverse

        proc = wormgate.WormProcess(script,
                exec_args=["one", "two", "three"],
                popen_kwargs=opts_to_pipe_output)

        try:
            (output, _) = proc.popen.communicate()
            self.assertEqual(output, b"three two one\n")

        finally:
            proc.cleanup()

    def test_cleanup(self):
        script = continuous_echo

        proc = wormgate.WormProcess(script, popen_kwargs=opts_to_pipe_output)

        try:
            time.sleep(.01)
            exitcode = proc.cleanup()
            (output, _) = proc.popen.communicate()
            self.assertEqual(exitcode, -15)             # Terminated by signal 15 (TERM)
            self.assertEqual(proc.popen.poll(), -15)    # Terminated by signal 15 (TERM)
            self.assertEqual(os.path.isfile(proc.execfile.name), False) # File is cleaned up
            self.assertEqual(output, b"Starting loop\n")

        finally:
            proc.cleanup()

class TestWormGateCore(unittest.TestCase):

    def test_start(self):
        script = show_args_reverse

        gate = wormgate.WormGateCore()

        try:
            proc = gate.start_process(script,
                    exec_args=["one", "two", "three"],
                    popen_kwargs=opts_to_pipe_output)

            self.assertEqual(len(gate.processes), 1)
        finally:
            gate.cleanup_all()

    def test_remove_finished(self):
        script = show_args_reverse

        gate = wormgate.WormGateCore()

        try:
            proc = gate.start_process(script,
                    exec_args=["one", "two", "three"],
                    popen_kwargs=opts_to_pipe_output)

            time.sleep(.02)

            exitcodes = gate.remove_finished()
            self.assertEqual(exitcodes, [0])

        finally:
            gate.cleanup_all()

    def test_cleanup_all(self):
        script = continuous_echo

        gate = wormgate.WormGateCore()

        try:
            proc = gate.start_process(script,
                    exec_args=[],
                    popen_kwargs=opts_to_pipe_output)

            time.sleep(.02)

            exitcodes = gate.cleanup_all()
            self.assertEqual(exitcodes, [-15])

        finally:
            gate.cleanup_all()

if __name__ == "__main__":
    unittest.main()
