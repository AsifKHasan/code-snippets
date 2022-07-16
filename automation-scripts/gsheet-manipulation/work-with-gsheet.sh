#!/usr/bin/env bash

# parameters
if [ $# -eq 0 ] 
then
  set echo off
  pushd ./src
  ./work-with-gsheet.py
else
  GSHEET=$1
  set echo off
  pushd ./src
  ./work-with-gsheet.py --gsheet ${GSHEET}
fi


if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
