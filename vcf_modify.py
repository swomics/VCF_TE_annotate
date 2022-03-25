import pysam
import argparse

def index_in_list(a_list, index):
    return()

def make_allele_key(a_list):
    if a_list[2] == "ref":
        key = 0
    else:
        if len(a_list) == 3:
            key = 1
        else:
            key = int(a_list[3])+1
    return(key)

def create_insert_extend(a_dict,ID_key,allele_key,data):
    if ID_key not in a_dict:
        a_dict[ID_key] = {allele_key: data}
    else:
        if allele_key not in a_dict[ID_key]:
            a_dict[ID_key][allele_key] = data
        else:
            a_dict[ID_key][allele_key].extend(data)

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--vcf", type=str,help="gff", action='store',required=True)
parser.add_argument("-b", "--bed", type=str,help="Repeatmasker bed file", action='store',required=True)

args = parser.parse_args()

f = open(args.bed,'r')

var_dict = dict()

for line in f:
    l = line.rstrip("\n")
    fields = l.split("\t")
    ID = fields[0].split("_")
    key = make_allele_key(ID)
    print(key,fields)
    #print(key)
    create_insert_extend(var_dict,ID[0]+ID[1],key,[fields[6],fields[7],fields[3],fields[2]])


print(var_dict)
#read the input file
myvcf=pysam.VariantFile(args.vcf,"r")

# Add the TE field to header. Say its a string and can take any no. of values.
myvcf.header.formats.add("TE",".","String","EDTA annotation class")
#myvcf.header.formats.add("FA",".","String","EDTA annotation family")
#myvcf.header.formats.add("LE",".","String","EDTA annotation length")


bcf_out = pysam.VariantFile(args.vcf+"anno.vcf", 'w', header=myvcf.header)
# An example showing how to add 'HP' information. Please explore further.
for variant in myvcf:

    for sample in variant.samples:
        try:
            allele1 = var_dict[variant.chrom+str(variant.pos)][variant.samples[sample].get('GT')[0]]
        except KeyError:
            allele1 = "."
        try:
            allele2 = var_dict[variant.chrom+str(variant.pos)][variant.samples[sample].get('GT')[1]]
        except KeyError:
            allele2 = "."
        variant.samples[sample]['TE'] = '_'.join(allele1)+","+ '_'.join(allele2)
        #if variant.chrom+str(variant.pos)
        #variant.samples[sample]['TE']=TE_data
        #print(variant.samples[sample].get('GT')[0])
    bcf_out.write(variant)
    print(variant)
