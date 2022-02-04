# RAM and run time benchmark for 1 cell. This emulate the original HTSeq.
# It's 1 cell from Domingo-Gonzalez et al. 2020, subsampled to 1M reads.

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
    bam_files_str = "{dirname}/8_cells/cell_1.bam".format(dirname=dirname)

    htseq_command = """
        python -m HTSeq.scripts.count \
            --mode intersection-nonempty \
            --quiet \
            --stranded no \
            --secondary-alignments ignore \
            --supplementary-alignments ignore \
            --counts_output {outfile} \
            --counts-output-sparse \
            --quiet \
            {bamfiles} \
            {gtffile}
    """

    time_runs = []
    for x in range(5):

        outfile = '{dirname}/htseq1_out/iter_{iter}_time.h5ad'.format(dirname=dirname, iter=x)
        run_htseq_command = htseq_command.format(bamfiles=bam_files_str, gtffile=gtf_file, outfile=outfile)

        t_start = time.time()
        run_htseq(run_htseq_command)
        t_end = time.time()
        
        t_delta = t_end - t_start
        time_runs.append(t_delta)

    stats_df = pd.DataFrame({"Duration": time_runs})
    stats_df["iteration"] = stats_df.index
    stats_df["unit"] = "seconds"
    stats_df.to_csv("{dirname}/htseq1_out/benchmark_time.csv".format(dirname=dirname), index=False)

    mem_usages = {}
    for x in range(5):

        outfile = '{dirname}/htseq1_out/iter_{iter}_ram.h5ad'.format(dirname=dirname, iter=x)
        run_htseq_command = htseq_command.format(bamfiles=bam_files_str, gtffile=gtf_file, outfile=outfile)

        mem_usage = memory_usage((run_htseq, (run_htseq_command,)),
            include_children=True, multiprocess=True, max_iterations=1, interval=10)
        mem_usages['iteration_{x}'.format(x=x)] = mem_usage

    print(mem_usages)

    # https://stackoverflow.com/questions/19736080/creating-dataframe-from-a-dictionary-where-entries-have-different-lengths
    stats_df = pd.DataFrame(pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in mem_usages.items() ])))
    stats_df["interval"] = stats_df.index
    stats_df["unit"] = "MB"
    stats_df.to_csv("{dirname}/htseq1_out/benchmark_ram.csv".format(dirname=dirname), index=False)


