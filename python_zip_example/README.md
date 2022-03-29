Packaging Python Code into a Single Executable File
==================================================

This is a "hello world" example of packaging Python code into an
executable zip file. It is based on the tutorial
"[A Simple Guide to Python Packaging](https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5)"
by Jie Feng.

The `make_python_zip_executable.sh` script will package up a directory
as an executable zip file. It takes the directory as its first argument.

    ./make_python_zip_executable.sh hello_world/

The script is very simple. All it does is this:

1. Zip up the directory
2. Prepend the "shebang" `#!/usr/bin/env python3`
    to the zip file, which tells bash to open the file with Python
3. Set the executable permission bit on the file

You can then run the resulting executable:

    ./hello_world.bin

<!-- vim: set tw=72 : -->
