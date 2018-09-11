#!/bin/bash
set -e

docker run -v $(pwd):/root/ -it slacker:local "$@"
