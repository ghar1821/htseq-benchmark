# Run HTSeq count barcode for the pbmc1k data.

import os

if __name__ == '__main__':    

    # Setup the files
    dirname = "/Users/z3535002/Documents/HTSeq/pbmc1k"
    gtf_file = dirname + '/refdata-gex-GRCh38-2020-A/genes/genes.gtf'

    bam_files_str = dirname + '/possorted_genome_bam.bam'

    outfile = dirname + '/output_htseq_fix_barcode/pbmc1k_counts.h5ad'

    samout = dirname + '/output_htseq_fix_barcode/pbmc1k_counts.sam'

    htseq_command = """
        python -m HTSeq.scripts.count_with_barcodes \
            --stranded yes \
            --secondary-alignments ignore \
            --supplementary-alignments ignore \
            --counts_output_sparse \
            --counts_output {outfile} \
            --samout {samout} \
            {bamfiles} \
            {gtffile}
    """.format(bamfiles = bam_files_str, gtffile = gtf_file, outfile = outfile, samout = samout)
    

    os.system(htseq_command)


    
        

    


