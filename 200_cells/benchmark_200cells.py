# RAM and run time benchmark for 200 cells from Domingo-Gonzalez et al. 2020.

import time
import pandas as pd
import os

from memory_profiler import memory_usage

def run_htseq(command):
    os.system(command)

if __name__ == '__main__':    

    # Setup the files
    dirname = "/Users/z3535002/Documents/HTSeq/parallel_vs_serial"
    gtf_file = dirname + '/mus_musculus_m39.gtf'


    bam_files = []
    with open("{dirname}/SRR_codes_for_200Cells_complete.txt".format(dirname=dirname), "r") as f:
        for line in f:
            bam_file = "{dirname}/200_cells/bam_files/{line}_aligned.bam".format(dirname=dirname, line=line.rstrip())
            bam_files.append(bam_file)

    bam_files_str = ' '.join(bam_files)
    ncpus = range(1, 9)

    htseq_command = """
        python -m HTSeq.scripts.count \
            --mode intersection-nonempty \
            --quiet \
            --stranded no \
            --secondary-alignments ignore \
            --supplementary-alignments ignore \
            --counts_output {outfile} \
            --counts-output-sparse \
            --nprocesses {ncpu} \
            {bamfiles} \
            {gtffile}
    """



    for ncpu in ncpus:

        print(ncpu)

        time_10_runs = []
        for x in range(5):

            outfile = '{dirname}/200_cells/out/ncpu_{ncpu}_iter_{iter}_time.h5ad'.format(dirname=dirname, ncpu=ncpu, iter=x)
            run_htseq_command = htseq_command.format(bamfiles=bam_files_str, gtffile=gtf_file, ncpu=ncpu, outfile=outfile)

            t_start = time.time()
            run_htseq(run_htseq_command)
            t_end = time.time()
            t_delta = t_end - t_start
            time_10_runs.append(t_delta)

            print(t_delta)

        stats_df = pd.DataFrame({"Duration": time_10_runs})
        stats_df["iteration"] = stats_df.index
        stats_df["unit"] = "seconds"
        stats_df.to_csv("{dirname}/200_cells/benchmark_time_ncpu_{ncpu}.csv".format(dirname=dirname, ncpu=ncpu), index=False)

        mem_usages = {}
        for x in range(5):

            outfile = '{dirname}/200_cells/out/ncpu_{ncpu}_iter_{iter}_ram.h5ad'.format(dirname=dirname, ncpu=ncpu, iter=x)
            run_htseq_command = htseq_command.format(bamfiles=bam_files_str, gtffile=gtf_file, ncpu=ncpu, outfile=outfile)

            mem_usage = memory_usage((run_htseq, (run_htseq_command,)),
                include_children=True, multiprocess=True, max_iterations=1, interval=10)
            mem_usages['iteration_{x}'.format(x=x)] = mem_usage

        print(mem_usages)

        # https://stackoverflow.com/questions/19736080/creating-dataframe-from-a-dictionary-where-entries-have-different-lengths
        stats_df = pd.DataFrame(pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in mem_usages.items() ])))
        stats_df["interval"] = stats_df.index
        stats_df["unit"] = "MB"
        stats_df.to_csv("{dirname}/200_cells/benchmark_ram_ncpu_{ncpu}.csv".format(dirname=dirname, ncpu=ncpu), index=False)

    
        

    


