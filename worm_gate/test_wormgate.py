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

class TestHttp(unittest.TestCase):

    GATE_STARTUP_TIME = 0.1

    def do_upload_test(self, curl_cmd, expect_response_code=None, expect_in_log=None):
        # Start a worm gate process.
        worm_gate_proc = subprocess.Popen(
                "python3 ./wormgate.py --port 8000 --loglevel DEBUG".split(),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(self.GATE_STARTUP_TIME)

        # Use curl to send a request to the gate.
        curl_proc = None
        curl_out = None
        try:
            curl_proc = subprocess.run(curl_cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            curl_out = curl_proc.stdout.decode()
        finally:
            # Terminate the gate process and wait for it to stop.
            worm_gate_proc.terminate()
            (gate_log, _) = worm_gate_proc.communicate()
            gate_log = gate_log.decode()

        # Format curl and log output for display on error
        output_display = f"\n\nCURL OUTPUT:\n{curl_out}\n\nGATE LOG:\n{gate_log}\n"

        # Test assertions

        self.assertEqual(curl_proc.returncode, 0,
                msg = "Expected zero (success) return code from curl process" + output_display)

        if expect_response_code:
            self.assertIn(f"HTTP/1.0 {expect_response_code}", curl_out,
                    msg = "Expected to see HTTP response code in curl output" + output_display)

        if expect_in_log:
            self.assertIn(expect_in_log, gate_log,
                    msg = "Expected to see specific output in server log" + output_display)

    def test_upload_content_length(self):
        curl_cmd = "curl -v -X POST http://localhost:8000/worm_entrance".split()
        curl_cmd = curl_cmd + ["--data-binary", hello_worm]
        # Curl's default is to use the Content-Length header.
        self.do_upload_test(curl_cmd,
                expect_response_code=200,
                expect_in_log="Hello, World!")

    def test_upload_chunked(self):
        curl_cmd = "curl -v -X POST http://localhost:8000/worm_entrance".split()
        curl_cmd = curl_cmd + ["--data-binary", hello_worm]
        # Use Transfer-Encoding instead of Content-Length when sending.
        curl_cmd = curl_cmd + ["-H", "Transfer-Encoding: chunked"]
        self.do_upload_test(curl_cmd,
                expect_response_code=200,
                expect_in_log="Hello, World!")

    def test_upload_bad(self):
        curl_cmd = "curl -v -X POST http://localhost:8000/worm_entrance".split()
        curl_cmd = curl_cmd + ["--data-binary", hello_worm]
        # Remove the Content-Length header without providing Transfer-Encoding.
        # The server will not know how to determine the end of the request.
        curl_cmd = curl_cmd + ["-H", "Content-Length:"]
        self.do_upload_test(curl_cmd,
                expect_response_code=400,
                expect_in_log="Unsupported encoding/length")

if __name__ == "__main__":
    unittest.main()
