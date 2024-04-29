input_dir=""
output_dir=""


for docx_file in "$input_dir"/*.docx; do
    base_name=$(basename "$docx_file")
    markdown_file="$output_dir/${base_name%.docx}.md"
    pandoc -f docx -t markdown "$docx_file" --mathjax -o "$markdown_file"
done