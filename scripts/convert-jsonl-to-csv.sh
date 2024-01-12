#!/bin/bash

jsonl_file=$1
csv_file=$2

if [ -z "$jsonl_file" ]; then
    echo "Usage: $0 <jsonl_file> <csv_file>"
    exit 1
fi

if [ -z "$csv_file" ]; then
    csv_file=${jsonl_file%.*}.csv
fi

echo "Converting $jsonl_file to $csv_file"
python3 -c "import pandas as pd; pd.read_json('$jsonl_file', lines=True).to_csv('$csv_file', index=False)"
