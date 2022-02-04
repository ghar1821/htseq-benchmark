# Re-run cellranger count on the pbmc data. Cellranger version 6.1.2.

cellranger count --id=count_pbmc1k \
   --transcriptome=/home/gputri/HTSeq/pbmc1k/refdata-gex-GRCh38-2020-A \
   --fastqs=/home/gputri/HTSeq/pbmc1k/pbmc_1k_v3_fastqs \
   --sample=pbmc_1k_v3 \
   --expect-cells=1000 \
   --localcores=16 \
   --localmem=64
