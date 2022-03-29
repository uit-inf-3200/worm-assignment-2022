Worm Gate code for INF-3203
==================================================

This is the _worm gate_ code for the Worm assignment
in UiT's INF-3203 course.

Author: Mike Murphy <michael.j.murphy@uit.no>

This README describes the technical details of the worm gate code and
its API. For a conceptual overview of the assignment, see the separate
assignment text.

- **THIS CODE IS A DELIBERATE SECURITY HOLE.**
- **DO NOT RUN THIS CODE ON ANY PUBLIC-FACING COMPUTER.**
- **DO NOT RUN THIS CODE AS A PRIVILEGED USER.**

Running the Worm Gate
--------------------------------------------------

The worm gate is an HTTP server written in Python (version 3).

The whole program is contained in one script, `wormgate.py`.
Run it with `python3`, or set the executable bit and run it directly.

    python3 wormgate.py --port 8000

The `--port` option is required.
For local testing, you will need to use different ports to run multiple
worm gates on one machine. For testing on the cluster, you will need to
use different ports to avoid colliding with your fellow students.
The [ephemeral port range](https://en.wikipedia.org/wiki/Ephemeral_port)
of 49152–65535 is a good range to pick from.

The worm gate keeps a list of other worm gates that are accessible.
This list is available to via the `/info` API.
To set that list, list running worm gate hosts on the command line:

    python3 wormgate.py --port 8000 localhost:8081 localhost:8082

The worm gate will filter its own name out of this list.
So if you're starting worm gates with a simple script,
you won't have to customize the list of gates each time.

To avoid clogging the cluster with forgotten worm gate processes, the
worm gate server will shut down automatically after a certain amount of
time has passed (default: 20 minutes). To adjust this, use the
`--die-after-seconds` argument.

If the server cannot accomplish a graceful shutdown,
it will wait a few more seconds (default: 2 seconds)
and then shutdown forcefully with `sys.exit(1)`.
To adjust this timeout, use the `--shutdown-grace-period` argument.

There are a few other command line options to set things like the server
log level, etc.
To get a list of options, run with the `--help` option:

    python3 wormgate.py --help

### Helper Scripts

The repository also includes a few helper scripts for starting and
stopping worm gates:

- `wormgates_start.sh`
    --- Starts several worm gates using a list of HOST:PORT pairs on
        standard input
- `wormgates_kill.sh`
    --- Kills worm gates using that same list
- `cluster_kill.sh`
    --- A merciless worm cleanup.
        Kills all of your process on the cluster,
        plus removes temporary worm segment files

Worm Gate HTTP API
--------------------------------------------------

### GET /info

A simple get to check that the server is running. Example:

```bash
curl -X GET http://localhost:8000/info
```

This will return a status JSON, similar to this:

```json
{
  "msg": "Worm gate running",
  "servername": "localhost:8080",
  "numsegments": 0,
  "other_gates": [
    "localhost:8081",
    "localhost:8082"
  ]
}
```

Elements:

- **`servername`**: the host:port of this worm gate server
- **`numsegments`**: the number of segments running on this worm gate
- **`other_gates`**: other worm gate host:port pairs (as listed on
  commend line at startup)

Your worm may use this information to decide where to propagate to next.

### POST /worm\_entrance -- Upload and run worm code

The body of the request will be saved as a binary on the host machine
and then executed.

Specifically, this call will:

1. Save the body to a temporary file in the RAM disk at `/dev/shm/`
2. Set the execute bit on that file
3. Run it

Reminder that this is an astoundingly unsafe thing to do.
**Do not run this code on any public-facing computer.**

Here is an example request that posts a two-line bash script.
You should see "Hello world" printed in the server's standard output.

```bash
curl -X POST http://localhost:8000/worm_entrance \
        -d '#!/bin/bash'$'\n''echo "Hello world"'
```

To pass arguments to the script, add them as `args` query parameters
to the HTTP request.
This is a two-line bash script that prints its arguments in reverse
order. You should see "three two one" printed in the server's standard
output.

```bash
curl -X POST 'http://localhost:8000/worm_entrance?args=one&args=two&args=three' \
        -d '#!/bin/bash'$'\n''echo "$3 $2 $1"'
```

### POST /kill\_worms --- Kill child worm processes

This example worm will keep running, printing "I am still running" to
stdout every 2 seconds.

```bash
curl -X POST http://localhost:8000/worm_entrance \
        -d '#!/bin/bash'$'\n''while true; do echo "I am still running"; sleep 2; done'
```

If you check the worm gate status you will see that it is still running.

```bash
curl -X GET http://localhost:8000/info
```

```json
{
  "msg": "Worm gate running",
  "servername": "localhost:8000",
  "numsegments": 1
}
```

Now you can kill the process by POST-ing to `/kill_worms`

```bash
curl -X POST http://localhost:8000/kill_worms
```

This will return a JSON that includes the exit codes of processes
killed.

```json
{
  "msg": "Child processes killed",
  "exitcodes": [
    -15
  ]
}
```

Negative exit codes indicate that they were killed via POSIX signal,
so -15 indicates that the process was killed via SIGTERM.
The worm gate will try SIGTERM first.
If the worm gate doesn't stop quickly, then it will use SIGKILL,
resulting in an exit code of -9.

Packaging Python Code to a Single Executable File
--------------------------------------------------

The worm gate operation assumes that all your code is in one executable
file.
If you are using libraries, you will have to package everything up
as one executable.

If you are using Python, you can zip up a code directory into a zip
file and then add a magic prefix to make it an executable.
See the tutorial
"[A Simple Guide to Python Packaging](https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5)"
by Jie Feng,
and the hello-world example here in the
[`python_zip_example/`](../python_zip_example/)
directory.

(Reminder: you can use any language you like for your worm, as long as
you can get it working in the worm gate on the cluster.)

Once you create your executable (in the example, `hello_world.bin`),
you can upload it to a running worm gate:

```bash
# Start a worm gate
python3 wormgate.py -p 8000 &
# Upload the zipped binary
curl -X POST http://localhost:8000/worm_entrance \
    --data-binary @../python_zip_example/hello_world.bin
```

<!-- vim: set tw=72 : -->
