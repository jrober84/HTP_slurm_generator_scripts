#!/usr/bin/python
from argparse import (ArgumentParser)
import os
import pandas as pd






def parse_args():
    "Parse the input arguments, use '-h' for help"
    parser = ArgumentParser(description='Create snippy bash scripts for use with local data')
    parser.add_argument('--input', type=str, required=True, help='tab delimited sample information file with the format sample_id,fwd_read,rev_read')
    parser.add_argument('--outdir', type=str, required=True,
                        help='Directory to write job files')
    parser.add_argument('--num_cpus', type=int, required=False,
                        help='Number of cpus for snippy to use default=4',default=4)
    parser.add_argument('-c', '--no_cleanup', required=False, help='Delete bam files and other large intermediate files',
                        action='store_true')
    parser.add_argument('-f', '--force', required=False, help='Overwrite existing directory',
                        action='store_true')

    return parser.parse_args()


def main():
    args = parse_args()

    sample_info = pd.read_csv(args.input, sep='\t', index_col='sample_id',
                              names=['sample_id','fwd_read','rev_read','outdir','reference'],header=0)


    parameters = "--cpus {} ".format( args.num_cpus )
    force = args.force
    if force:
        parameters += "--force "
    nocleanup = args.no_cleanup
    if not nocleanup:
        parameters += "--cleanup "
    outdir = args.outdir
    if not os.path.isdir(outdir):
        print('Error {} directory does not exist, please check path or create it and try again')

    for sample_id, row in sample_info.iterrows():
        outdir = row['outdir']
        original_fwd_read = row['fwd_read']
        original_rev_read = row['rev_read']
        reference_file = row['reference']
        snippy_dir = os.path.join(outdir,"{}_snippy".format(sample_id))
        bash_string = "#!/bin/sh\n"
        bash_string = bash_string + "snippy --prefix {} --outdir {} --ref {} --R1 {} --R2 {} --quiet {}\n".format(sample_id,snippy_dir,reference_file,original_fwd_read,original_rev_read,parameters)

        target = open(os.path.join(outdir,"{}.sh".format(sample_id)), 'w')
        target.write(bash_string)
        target.close()



# call main function
if __name__ == '__main__':
	main()
