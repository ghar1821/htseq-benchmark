#!/bin/bash

# Downloaded one for the 1 cell
# parallel-fastq-dump --sra-id SRR11435997 --threads 4 --outdir raw_files --split-files --gzip

# Download the rest for 200 cells
while IFS= read -r line; do
    echo "Processing $line"
    # prefetch $line
    parallel-fastq-dump --sra-id $line --threads 4 --outdir raw_files --split-files --gzip
done < "$1"

