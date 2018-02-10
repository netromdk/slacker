#!/bin/sh
REAL_PATH=$(readlink $0)
if [ ! -z ${REAL_PATH} ]; then
  REAL_DIR="$(dirname ${REAL_PATH})"
else
  REAL_DIR="$(pwd)/$(dirname $0)"
fi
cd ${REAL_DIR}

if [ ! -d .venv ]; then
  echo "Make sure to run 'make setup' in the slacker folder first!"
  exit -1
fi

source .venv/bin/activate
./slacker.py "$@"
