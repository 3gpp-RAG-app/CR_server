#!/bin/bash

input_dir=""
output_dir=""


mkdir -p "$output_dir"

for docx_file in "$input_dir"/*.docx; do
    base_name=$(basename "$docx_file")
    html_file="$output_dir/${base_name%.docx}.html"
    pandoc -f docx -t html "$docx_file" -o "$html_file"
done
