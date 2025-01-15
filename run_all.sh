#!/bin/bash

# Check if the required arguments are passed
if [ "$#" -lt 4 ]; then
    echo "Usage: ./run_all.sh <start_url> <output_file> <max_pages> <max_depth>"
    exit 1
fi

# Assign arguments to variables
START_URL=$1
OUTPUT_FILE=$2
MAX_PAGES=$3
MAX_DEPTH=$4

echo "[INFO] Running scraper with the following parameters:"
echo "       Start URL: $START_URL"
echo "       Output File: $OUTPUT_FILE"
echo "       Max Pages: $MAX_PAGES"
echo "       Max Depth: $MAX_DEPTH"

# Run the scraper
python src/scraper.py "$START_URL" "$OUTPUT_FILE" --max_pages "$MAX_PAGES" --max_depth "$MAX_DEPTH"
if [ $? -ne 0 ]; then
    echo "[ERROR] Scraper failed. Exiting."
    exit 1
fi
echo "[INFO] Scraper completed."

# Run the cleaner
echo "[INFO] Running cleaner on file: $OUTPUT_FILE"
python src/clean_data.py "$OUTPUT_FILE"
if [ $? -ne 0 ]; then
    echo "[ERROR] Cleaner failed. Exiting."
    exit 1
fi
echo "[INFO] Cleaner completed."

echo "[INFO] All tasks completed successfully."
