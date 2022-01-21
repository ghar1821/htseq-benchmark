seqtk sample -s42 SRR11435997_1.fastq.gz 1000000 > ../subsample/sub_SRR11435997_1.fastq
seqtk sample -s42 SRR11435997_2.fastq.gz 1000000 > ../subsample/sub_SRR11435997_2.fastq

seqtk sample -s42 SRR069883_1.fastq.gz $t > subsampled/${t}_1.fastq
seqtk sample -s42 SRR069883_2.fastq.gz $t > subsampled/${t}_2.fastq

gzip subsampled/${t}_1.fastq
gzip subsampled/${t}_2.fastq

# This is for generating the genome
STAR \
        --runThreadN 4 \
        --runMode genomeGenerate \
        --genomeDir star_index \
        --genomeFastaFiles Mus_musculus.GRCm39.dna.primary_assembly.fa \
        --sjdbGTFfile Mus_musculus.GRCm39.105.chr.gtf \
        --sjdbOverhang 99


STAR \
        --runThreadN 4 \
	    --runMode alignReads \
	    --genomeDir /home/gputri/HTSeq/star_files/drosophila/genome \
	    --readFilesIn subsampled/${t}_1.fastq.gz  subsampled/${t}_2.fastq.gz \
	    --readFilesCommand zcat \
	    --outFileNamePrefix ${outdir} \
	    --outSAMtype BAM Unsorted \
	    --outReadsUnmapped Fastx \

# NOTE the options starting from outFilterType until alignMatesGapMax is the ENCODE standard. Consult the STAR manual.
# Used the following for scRNAseq
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
        
