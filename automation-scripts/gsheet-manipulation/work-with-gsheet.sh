#!/usr/bin/env bash
# work with gsheet

# parameters
GSHEET=$1

set echo off

pushd ./src
./work-with-gsheet.py --gsheet ${DOCUMENT}

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
