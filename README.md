# VCF_TE_annotate
Some rudimentary scripts to annotate vcf variants produced by pangenome graph approaches using the output of repeat annotation tools such as EDTA.

I was unable to find an existing tool that could associate inserted/deleted sequences present in VCF records with a Transposable element library. The script should provide text entries under the vcf tag ("TE") for each sample. The record should also be able to handle multiple repeat annotations for a single allele and also multiallelic entries.

vcf_anno.py is simply a wrapper for RepeatMasker - it pulls out the fasta entries for the individual allele sequences in a vcf and runs the masking on them. 

vcf_modify.py  uses the output of this RepeatMasking step (after filtering with the RM2bed script with preferred overlap handling) to attach the results to the individual genotypes within the vcf .

For example:
"FR989862.1      131726  FR989862.1-131726-SNV-0-1       A       T       60      .       ID=FR989862.1-131726-SNV-0-1    GT:TE   0|1:DNA_LTR_TE_00005245_87,DNA_LTR_TE_00005245_87   0|0:DNA_LTR_TE_00005245_87,DNA_LTR_TE_00005245_87       1|1:DNA_LTR_TE_00005245_87,DNA_LTR_TE_00005245_87       0|1:DNA_LTR_TE_00005245_87,DNA_LTR_TE_00005245_87   0|1:DNA_LTR_TE_00005245_87,DNA_LTR_TE_00005245_87       1|1:DNA_LTR_TE_00005245_87,DNA_LTR_TE_00005245_87   0|1:DNA_LTR_TE_00005245_87,DNA_LTR_TE_00005245_87"

The vcf file was generated with the Pangenie make pangenome from assemblies script. EDTA was used to annotate each individual pangenome haplotype to create a pangenome TE library. These scripts aim to apply the EDTA repeat library to the vcf to facilitate viewing in IGV and to help calculate population frequencies of specific repeat families.

