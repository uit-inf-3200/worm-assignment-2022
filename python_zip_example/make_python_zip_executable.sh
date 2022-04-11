#!/bin/bash

# Show commands as they're being run
set -x

# DIR is parameter $1 with any trailing slash removed:
# e.g. "hello_world/" becomes "hello_world"
DIR="${1%/}"
ZIP="$DIR.zip"
EXEC="$DIR.bin"

# Remove previously generated files
rm "$ZIP" "$EXEC"

# Zip up the python example
(cd "$DIR" && zip -r ../"$ZIP" *)

# Start a new file with the python3 shebang line
echo '#!/usr/bin/env python3' > "$EXEC"
# Dump the contents of the zip into it, after the shebang
cat "$ZIP" >> "$EXEC"

# Set the executable bit
chmod u+x "$EXEC"
