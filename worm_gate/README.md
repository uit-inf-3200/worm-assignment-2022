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

Quick Start
--------------------------------------------------

### Hello Gate

The worm gate is a simple HTTP server.

Here, we start a worm gate server on port 8000:

```
$ ./wormgate.py --port 8000
INFO:myhost:8000-wormgate:Starting server on port 8000.
```

To check that it's running we can `GET /info`:

```
$ curl -X GET http://localhost:8000/info
{
  "msg": "Worm gate running",
  "servername": "myhost:8000",
  "numsegments": 0,
  "other_gates": []
}
```

### Hello Worm

The worm gate accepts uploaded binaries and runs them.

Here is a hello-world bash script, `hello.sh`:

```bash
#!/bin/bash
echo 'hello world'
```

To upload and run it, we can `POST` to `/worm_entrance`:

```
$ curl -X POST http://localhost:8000/worm_entrance --data-binary @hello.sh
Worm segment uploaded and started
```

In the worm gate's server log,
we should see log messages that it is starting the segment process,
plus the segment process's "hello world" output
(note: this example log output is simplified):

```
INFO:myhost:8000-wormgate:Wrote executable to /dev/shm/inf3203_worm_assignment_f2r13jtk
INFO:myhost:8000-wormgate:Started subprocess. PID 757996. Command: ['/dev/shm/inf3203_worm_assignment_f2r13jtk'].
127.0.0.1 - - [09/Apr/2022 22:05:34] "POST /worm_entrance HTTP/1.1" 200 -
hello world
```

### Hello Args

The worm-entrance API can pass command-line arguments to the segment
process.

Here is a bash script that repeats its arguments, `echo_args.sh`:

```bash
#!/bin/bash
echo "Hello args" "$@"
```

We pass parameters by adding query parameters to the URL
(be sure to quote the URL because `&` is a command character in bash):

```
$ curl -X POST 'http://localhost:8000/worm_entrance?args=1&args=2&args=3' --data-binary @echo_args.sh
Worm segment uploaded and started
```

The arguments should be visible in the server log (output simplified):

```
INFO:myhost:8000-wormgate:Wrote executable to /dev/shm/inf3203_worm_assignment_769jhf6_
INFO:myhost:8000-wormgate:Started subprocess. PID 776856. Command: ['/dev/shm/inf3203_worm_assignment_769jhf6_', '1', '2', '3'].
127.0.0.1 - - [09/Apr/2022 22:16:07] "POST /worm_entrance?args=1&args=2&args=3 HTTP/1.1" 200 -
Hello args 1 2 3
```

### Goodbye Worm

The worm gate can kill worm segments.

Here is a bash script that never ends, `forever.sh`:

```bash
#!/bin/bash
while true; do
    echo "I am still running"
    sleep 2
done
```

#### Upload and run

```
$ curl -X POST 'http://localhost:8000/worm_entrance' --data-binary @forever.sh
Worm segment uploaded and started
```

```
INFO:myhost:8000-wormgate:Wrote executable to /dev/shm/inf3203_worm_assignment_6itkwgn2
INFO:myhost:8000-wormgate:Started subprocess. PID 814861. Command: ['/dev/shm/inf3203_worm_assignment_6itkwgn2'].
127.0.0.1 - - [09/Apr/2022 22:37:35] "POST /worm_entrance HTTP/1.1" 200 -
I am still running
I am still running
```

#### Check

The `GET /info` call shows that one segment is running:

```
$ curl -X GET http://localhost:8000/info
{
  "msg": "Worm gate running",
  "servername": "myhost:8000",
  "numsegments": 1,
  "other_gates": []
}
```

```
I am still running
127.0.0.1 - - [09/Apr/2022 22:37:38] "GET /info HTTP/1.1" 200 -
I am still running
```

#### Kill

To kill the segment, we can `POST` to `/kill_worms`:

```
$ curl -X POST 'http://localhost:8000/kill_worms'
{
  "msg": "Child processes killed",
  "exitcodes": [
    -15
  ]
}
```

```
I am still running
I am still running
INFO:myhost:8000-wormgate:WormProcess{PID=814861} still running, terminating
INFO:myhost:8000-wormgate:Removing executable /dev/shm/inf3203_worm_assignment_6itkwgn2
127.0.0.1 - - [09/Apr/2022 22:37:44] "POST /kill_worms HTTP/1.1" 200 -
```

### Hello Reflection

Your worm segment will need to read its own code in order to replicate.
In a Unix system, an executable can find itself by examining
command-line argument zero.

Here is a script that reads itself and quotes its own code back to you,
`arg0.sh`:

```bash
#!/bin/bash
echo "Hello this is the worm"
echo "My executable file is $0"
echo "I can read and quote my own code:"
echo "####################"
sed 's/^/# /' $0
echo "####################"
```

```
$ curl -X POST 'http://localhost:8000/worm_entrance' --data-binary @arg0.sh
Worm segment uploaded and started
```

```
INFO:myhost:8000-wormgate:Wrote executable to /dev/shm/inf3203_worm_assignment_uz2wi6cf
INFO:myhost:8000-wormgate:Started subprocess. PID 907917. Command: ['/dev/shm/inf3203_worm_assignment_uz2wi6cf'].
127.0.0.1 - - [09/Apr/2022 23:29:36] "POST /worm_entrance HTTP/1.1" 200 -
Hello this is the worm
My executable file is /dev/shm/inf3203_worm_assignment_uz2wi6cf
I can read and quote my own code:
####################
# #!/bin/bash
# echo "Hello this is the worm"
# echo "My executable file is $0"
# echo "I can read and quote my own code:"
# echo "####################"
# sed 's/^/# /' $0
# echo "####################"
####################
```

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

Helper Scripts
--------------------------------------------------

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

### Piping Input to wormgates\_start.sh and wormgates\_kill.sh

The matching `wormgates_start.sh` and `wormgates_kill.sh` scripts take
their lists via standard input. The idea is that you can have a list
of HOST:PORT pairs in a text file and then pipe it into the scripts.

For example, here is a one-liner that creates a list of three
localhost:port pairs with random ports from the ephemeral port range:

```bash
$ shuf -i 49152-65535 -n 3 | sed 's/^/localhost:/'
localhost:65140
localhost:56844
localhost:60846
```

We can save that as a text file, and use it to start our worm gates
(output simplified):

```bash
$ shuf -i 49152-65535 -n 3 | sed 's/^/localhost:/' > host_list.txt
$ cat host_list.txt | ./wormgates_start.sh
localhost:54176 -- + ./wormgate.py -p 54176 localhost:54176 localhost:62137 localhost:57040
localhost:62137 -- + ./wormgate.py -p 62137 localhost:54176 localhost:62137 localhost:57040
localhost:57040 -- + ./wormgate.py -p 57040 localhost:54176 localhost:62137 localhost:57040
INFO:myhost:54176-wormgate:Starting server on port 54176.
INFO:myhost:62137-wormgate:Starting server on port 62137.
INFO:myhost:57040-wormgate:Starting server on port 57040.
```

The script's output shows the command lines it uses to start each gate
(after the "`-- +`" characters). We can also see how it passes all of
the other host:port pairs to each worm gate at start up. If the host
names are anything besides `localhost`, the script will use `ssh` to
start the gate on the appropriate host rather than executing it locally
(output simplified):

```bash
[mmu019@uvcluster worm_gate]$ cat host_list.txt | ./wormgates_start.sh
compute-1-1:60000 -- + ssh -f compute-1-1 ./wormgate.py -p 60000 compute-1-1:60000 compute-2-1:60000 compute-3-1:60000
compute-2-1:60000 -- + ssh -f compute-2-1 ./wormgate.py -p 60000 compute-1-1:60000 compute-2-1:60000 compute-3-1:60000
compute-3-1:60000 -- + ssh -f compute-3-1 ./wormgate.py -p 60000 compute-1-1:60000 compute-2-1:60000 compute-3-1:60000
INFO:compute-1-1:60000-wormgate:Starting server on port 60000.
INFO:compute-3-1:60000-wormgate:Starting server on port 60000.
INFO:compute-2-1:60000-wormgate:Starting server on port 60000.
```

### Passing Additional Worm Gate Arguments

Any additional arguments on the `./wormgates_start.sh` command line
will be passed to the worm gates between the `-p` port argument and the
list of host:port pairs. To decrease the log level for all launched
worm gates, we can add the `--loglevel` argument (output simplified):

```bash
$ cat host_list.txt | ./wormgates_start.sh --loglevel WARN
localhost:54176 -- + ./wormgate.py -p 54176 --loglevel WARN localhost:54176 localhost:62137 localhost:57040
# (...and so on...)
```

### Kill, Kill, Kill!

The `wormgates_kill.sh` script takes its input via pipe in the same way,
though this time there are no additional arguments to pass.
(output simplified):

```bash
$ cat host_list.txt | ./wormgates_kill.sh
localhost:54176 -- + pkill -f wormgate.py
localhost:62137 -- + pkill -f wormgate.py
localhost:57040 -- + pkill -f wormgate.py
INFO:myhost:54176-wormgate:Got system signal 15, SIGTERM.
INFO:myhost:62137-wormgate:Got system signal 15, SIGTERM.
INFO:myhost:57040-wormgate:Got system signal 15, SIGTERM.
```

And, like the startup script, it will use SSH if the hostname is not
`localhost` (output simplified):

```bash
[mmu019@uvcluster worm_gate]$ cat host_list.txt | ./wormgates_kill.sh
compute-1-1:60000 -- + ssh -f compute-1-1 pkill -f wormgate.py
compute-2-1:60000 -- + ssh -f compute-2-1 pkill -f wormgate.py
compute-3-1:60000 -- + ssh -f compute-3-1 pkill -f wormgate.py
INFO:compute-1-1:60000-wormgate:Got system signal 15, SIGTERM.
INFO:compute-2-1:60000-wormgate:Got system signal 15, SIGTERM.
INFO:compute-3-1:60000-wormgate:Got system signal 15, SIGTERM.
```

### "I say we take off and nuke the site from orbit": cluster\_kill.sh

The `cluster_kill.sh` script only works on the cluster. It takes no
arguments because it is much more aggressive. It uses `ssh` to go into
every node in the cluster one by one and kill every process owned by
your user (output simplified):

```bash
$ ./cluster_kill.sh
Connection to compute-3-0 closed by remote host.
Connection to compute-3-0 closed by remote host.
# (...and so on...)
```

The "connection closed by remote host" messages show up because the kill
command kills all user processes on the host, including the SSH session.
It's normal to see a lot of them.

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

#### Request body becomes worm executable

The body of the request becomes the executed binary.
Use raw data (e.g. curl `--data-binary`),
not form data (e.g. curl `--form`).
Example curl line:

```
curl -X POST http://localhost:8000/worm_entrance --data-binary @segment.exe
```

#### Query parameter `args` becomes command-line arguments

Add an `args` query parameter to pass a command-line argument to the
worm segment executable. Repeat it to add more arguments.

| Query string             |   | Command line              |
|--------------------------|---|---------------------------|
| `?args=hello`            | → | `segment.exe hello`       |
| `?args=hello&args=world` | → | `segment.exe hello world` |
| `?args=--port&args=9000` | → | `segment.exe --port 9000` |


Example curl line:

```
curl -X POST 'http://localhost:8000/worm_entrance?args=--port&args=9000' \
    --data-binary @segment.exe
```

The binary `segment.exe` will be uploaded and executed like:

```
./segment.exe --port 9000
```

### POST /kill\_worms --- Kill child worm processes

This call will simply kill any worm segment processes that the worm
gate has started.

1. The worm gate will send SIGTERM to each worm segment process.
2. It will wait a few seconds.
3. Any worm processes that are still running will be forcefully
    killed with SIGKILL.

The response will be a JSON object with info about the exit codes
of the worm segment processes:

```json
{
  "msg": "Child processes killed",
  "exitcodes": [
    -15
  ]
}
```

Packaging Python Code to a Single Executable File
--------------------------------------------------

The worm gate operation assumes that all your code is in one executable
file.
If you are using libraries, you will have to package everything up
as one executable.

If you are using Python, you can zip up a code directory into a zip
file and then add a magic prefix to make it an executable.
See the tutorial
"[Execute a Directory/Zip File in Python](https://medium.com/python-features/execute-a-directory-zip-file-in-python-3c33c26cec30)"
by Rachit Tayal
and the hello-world example here in the
[`python_zip_example/`](../python_zip_example/)
directory.

(Reminder that you can use any language you like for your worm, as long
as you can get it working in the worm gate on the cluster.
You may find that a compiled language is a better fit for this project.)

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
