# Use Seqtk to subsample the FASTQ files downloaded from Domingo-Gonzalez et al. 2020
# The 1 cell SRR code is SRR11435997
# Thanks biostar: https://www.biostars.org/p/6544/

seqtk sample -s42 SRR11435997_1.fastq.gz 1000000 > ../subsample/sub_SRR11435997_1.fastq
seqtk sample -s42 SRR11435997_2.fastq.gz 1000000 > ../subsample/sub_SRR11435997_2.fastq


STAR \
        --runThreadN 32 \
        --runMode alignReads \
        --genomeDir ../../star_files/genome \
        --readFilesIn sub_SRR11435997_1.fastq.gz  sub_SRR11435997_2.fastq.gz \
        --readFilesCommand zcat \
        --outFileNamePrefix star_alignment/ \
        --outSAMtype BAM Unsorted \
        --outReadsUnmapped Fastx \
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
        
