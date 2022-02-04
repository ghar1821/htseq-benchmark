# The FASTA and GTF files are downloaded from ensembl (https://asia.ensembl.org/index.html)

# This is for generating the genome
STAR \
        --runThreadN 4 \
        --runMode genomeGenerate \
        --genomeDir star_index \
        --genomeFastaFiles Mus_musculus.GRCm39.dna.primary_assembly.fa \
        --sjdbGTFfile Mus_musculus.GRCm39.105.chr.gtf \
        --sjdbOverhang 99
