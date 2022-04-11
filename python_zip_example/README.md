Packaging Python Code into a Single Executable File
==================================================

This is a "hello world" example of packaging Python code into an
executable zip file. It is based on the tutorial
"[Execute a Directory/Zip File in Python](https://medium.com/python-features/execute-a-directory-zip-file-in-python-3c33c26cec30)"
by Rachit Tayal.

Quick Summary
--------------------------------------------------

The `make_python_zip_executable.sh` script packages a multi-file Python
project directory as an executable zip file.
It takes the directory as its first argument.

    ./make_python_zip_executable.sh hello_world/

The script is very simple. All it does is this:

1. Zip up the directory
2. Prepend the "shebang" `#!/usr/bin/env python3`
    to the zip file, which tells bash to open the file with Python
3. Set the executable permission bit on the file

You can then run the resulting executable:

    ./hello_world.bin


How it Works
--------------------------------------------------

### Hello Directory

The `hello_world/` directory is a multi-file,
multi-module Python project.
Execution starts with the file `hello_world/__main__.py` .
We can run the project by pointing Python at the directory:

```bash
$ python3 hello_world/
Hello, World!
This string comes from hello_world/example_module.py.
This string comes from a resource file.
```

### Hello Zip

We can also pack this directory into a zip file, and Python can still
run it.

```bash
# Move into the subdirectory
$ cd hello_world/

# Zip up the contents
$ zip -r ../hello_world.zip *
updating: example_module.py (stored 0%)
updating: __main__.py (deflated 38%)
updating: resources/ (stored 0%)
updating: resources/__init__.py (deflated 22%)
updating: resources/example_resource.txt (stored 0%)

# Back to the original directory
$ cd ..

# Run from the zip file
$ python3 hello_world.zip
Hello, World!
This string comes from hello_world.zip/example_module.py.
This string comes from a resource file.
```

### Hello Bash

It would be nice to be able to execute this zip file directly from
the command line like a typical compiled executable or shell script.
However, bash does not know how to execute a zip file.

```bash
# Try to run it naively
$ ./hello_world.zip
bash: ./hello_world.zip: Permission denied

# Set the executable bit
$ chmod u+x hello_world.zip

# Try again
$ ./hello_world.zip
invalid file (bad magic number): Exec format error
```

### Hello Shebang

To tell bash what program to open a script with,
we use a "shebang" line.
Surely you've seen these at the top of scripts:

- `#!/bin/bash` = "this is a bash script, run it with `/bin/bash`"
- `#!/usr/bin/env python3` = "this is a python script, use `env` to find
  the `python3` interpreter, and run it with that"

We can also do that with our zip file:

```bash
# Create new file with the shebang
$ echo '#!/usr/bin/env python3' > hello_world.bin

# Append the contents of the zip to the new file
$ cat hello_world.zip >> hello_world.bin
```

If we compare a hex dump of the original zip file and the new .bin file,
we can see that it is the same binary data, with a shebang line at the
front:

```bash
# Original zip file
# PK 0x03 0x04 are the "magic number" bytes that mark a zip file.
# ('PK' because the first zip program was PKZIP, by Phil Katz.)
$ xxd hello_world.zip | head -n 5
00000000: 504b 0304 0a00 0000 0000 0aa9 7350 68e6  PK..........sPh.
00000010: b70b 3b00 0000 3b00 0000 1100 1c00 6578  ..;...;.......ex
00000020: 616d 706c 655f 6d6f 6475 6c65 2e70 7955  ample_module.pyU
00000030: 5409 0003 34d1 735e e0d0 5362 7578 0b00  T...4.s^..Sbux..
00000040: 0104 e803 0000 04e8 0300 004d 4f44 554c  ...........MODUL

# New file with shebang at the start
# You can see the shebang, followed by a newline (0x0a),
# the zip magic number (PK 0x03 0x04), and the rest of the data.
$ xxd hello_world.bin | head -n 5
00000000: 2321 2f75 7372 2f62 696e 2f65 6e76 2070  #!/usr/bin/env p
00000010: 7974 686f 6e33 0a50 4b03 040a 0000 0000  ython3.PK.......
00000020: 000a a973 5068 e6b7 0b3b 0000 003b 0000  ...sPh...;...;..
00000030: 0011 001c 0065 7861 6d70 6c65 5f6d 6f64  .....example_mod
00000040: 756c 652e 7079 5554 0900 0334 d173 5ee0  ule.pyUT...4.s^.
```

Now we can run the .bin file:

```bash
# Set the executable bit
$ chmod u+x hello_world.bin

# Run it
$ ./hello_world.bin
Hello, World!
This string comes from ./hello_world.bin/example_module.py.
This string comes from a resource file.
```

1. You tell bash, "run `hello_world.bin`"
2. The shebang tells bash, "run this with Python"
3. Python knows how to read the zip, even with the shebang.

### Hello Script

The above steps are automated in the script
`make_python_zip_example.sh`:

```bash
$ ./make_python_zip_executable.sh hello_world/
+ DIR=hello_world
+ ZIP=hello_world.zip
+ EXEC=hello_world.bin
+ cd hello_world
+ zip -r ../hello_world.zip example_module.py __main__.py resources
  adding: example_module.py (stored 0%)
  adding: __main__.py (deflated 38%)
  adding: resources/ (stored 0%)
  adding: resources/__init__.py (deflated 22%)
  adding: resources/example_resource.txt (stored 0%)
+ echo '#!/usr/bin/env python3'
+ cat hello_world.zip
+ chmod u+x hello_world.bin

$ ./hello_world.bin
Hello, World!
This string comes from ./hello_world.bin/example_module.py.
This string comes from a resource file.
```

<!-- vim: set tw=72 : -->
