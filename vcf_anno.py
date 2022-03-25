from pysam import VariantFile
import argparse
import subprocess

def Write_vcf_inserts(args):
    f = open(args.output, 'w')
    # Open input, add FILTER header, and open output file
    bcf_in = VariantFile(args.vcf)  # auto-detect input format

    for rec in bcf_in:
        #print(list(rec.ref))
        if len(rec.ref) > args.min:
            #print("Ref allele "+rec.ref)
            f.write(">"+rec.chrom+"_"+str(rec.pos)+"\n"+rec.ref+"\n")
        for allele in rec.alts:
            if len(allele) > args.min:
                f.write(">"+rec.chrom+"_"+str(rec.pos)+"\n"+allele+"\n")
    f.close()


def run_repeatMasker(args):
    subprocess.run(["RepeatMasker","-pa",args.threads,"-lib",args.seq_lib," -e ncbi -q -no_is -norna -nolow -div 40 ",args.output])


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--vcf", type=str,help="gff", action='store',required=True)
parser.add_argument("-m", "--min", type=int,help="minimum allele length", action='store',required=True)
parser.add_argument("-o", "--output", type=str,help="out_file", action='store',required=True)
parser.add_argument("-s", "--seq_lib", type=str,help="Sequence library (e.g. EDTA fasta output)", action='store',required=True)
parser.add_argument("-t", "--threads", type=str,help="num threads", action='store',required=True)

args = parser.parse_args()

#run vcf parse
Write_vcf_inserts(args)
#run repeatmasker
run_repeatMasker(args)
