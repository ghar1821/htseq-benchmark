#!/bin/bash

dirname=/home/gputri/HTSeq
genomedir=$dirname/star_files/genome
readfilesdir=$dirname/parallel_vs_serial/raw_files
outdir=$dirname/parallel_vs_serial/star_out/

# NOTE, the STAR parameters are predominantly based on the script in the paper.

while IFS= read -r line; do
    outdir=$dirname/parallel_vs_serial/star_out/$line/
    mkdir $outdir

    STAR \
        --runThreadN 32 \
        --runMode alignReads \
        --genomeDir $genomedir \
        --readFilesIn $readfilesdir/${line}_1.fastq.gz  $readfilesdir/${line}_2.fastq.gz \
        --readFilesCommand zcat \
        --outFileNamePrefix $outdir \
        --outSAMtype BAM Unsorted \
        --outFilterType BySJout \
        --outFilterMultimapNmax 20 \
        --alignSJoverhangMin 8 \
        --alignSJDBoverhangMin 1 \
        --outFilterMismatchNmax 999 \
        --outFilterMismatchNoverLmax 0.04 \
        --alignIntronMin 20 \
        --alignIntronMax 1000000 \
        --alignMatesGapMax 1000000 \
        --outSAMstrandField intronMotif \
        --outSAMattributes NH HI AS NM MD \
        --outFilterMatchNminOverLread 0.4 \
        --outFilterScoreMinOverLread 0.4 \
        --outReadsUnmapped Fastx
        # DOES NOT WORK
        #--clip3pAdapterSeq CTGTCTCTTATACACATCT \
done < $1
