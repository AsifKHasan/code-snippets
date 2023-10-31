#!/usr/bin/env bash
# bb-data->chart

PYTHON=python3

# bb-data-to-chart
pushd ./src
${PYTHON} bb-data-to-chart.py

if [ ${?} -ne 0 ]; then
  popd && exit 1
else
  popd
fi
