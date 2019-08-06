#!/bin/bash
#$ -V
#$ -S /bin/bash
#$ -cwd
#$ -m as
#$ -M m.m.nieboer@umcutrecht.nl
#$ -l h_vmem=16G
#$ -l h_rt=04:00:00
#$ -e naive_err
#$ -o naive_out

python compareShuffledPerformanceToNaive.py Output/ShuffledCodingNonCoding/geneCodingSVPairs_somatic_me_12072019_shuffled.txt_ Output/ShuffledCodingNonCoding/geneSVPairs_somatic_me_12072019_shuffled.txt__codingPairDEGs.npy ../../data/genes/CCGC.tsv ../../data/svs/brca_tcga_parsed_05022019.txt ../../data/tads/HMEC_Lieberman-raw_TADs.bed ../../data/genes/breastCancerCausalGenes.txt 0 ../../data/expression/gdac.broadinstitute.org_BRCA.Merge_rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.Level_3.2016012800.0.0/BRCA.rnaseqv2__illuminahiseq_rnaseqv2__unc_edu__Level_3__RSEM_genes_normalized__data.data.txt