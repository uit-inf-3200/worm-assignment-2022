#!/bin/bash

# Starts wormgates from list of HOST:PORT pairs on standard input
# Passes additional command-line arguments to the gates

GATESCRIPT="$(readlink -f wormgate.py)"

mapfile -t GATES        # read stdin to GATES array

for LINE in "${GATES[@]}"
do
    if [[ "$LINE" =~ ^[a-zA-Z0-9_-]+:[0-9]+$ ]]
    then
        HOST="$(echo "$LINE" | cut -d':' -f1)"
        PORT="$(echo "$LINE" | cut -d':' -f2)"

        echo -n "$HOST:$PORT -- "
        if [[ "$HOST" == "localhost" ]]
        then
            (set -x; "$GATESCRIPT" -p "$PORT" "$@" "${GATES[@]}" &)
        else
            (set -x; ssh -f "$HOST" "$GATESCRIPT" -p "$PORT" "$@" "${GATES[@]}")
        fi

    else
        echo "Skipping line that does not match host:port format: $LINE"
    fi
done
