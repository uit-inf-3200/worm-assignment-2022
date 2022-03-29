#!/bin/bash

set -x

DIR="${1%/}"
ZIP="$DIR.zip"
EXEC="$DIR.bin"

# Remove previously generated files
rm "$ZIP" "$EXEC"

# Zip up the python example
(cd "$DIR" && zip -r - *) > "$ZIP"

# Prepend a python3 shebang and save that as the executable
echo '#!/usr/bin/env python3' | cat - "$ZIP" > "$EXEC"

# Set the executable permissions
chmod u+x "$EXEC"
