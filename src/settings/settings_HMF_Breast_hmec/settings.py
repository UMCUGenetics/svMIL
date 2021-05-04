general = dict(
	source = 'HMF',
	cancerType = "Breast",
	shuffleTads = False,
	crd = False,
	gtexControl = False,
	geneENSG = False,
	bagThreshold = 700,
)
files = dict(
	svDir = "/hpc/cuppen/shared_resources/HMF_data/DR-104/data/somatics/",
	snvDir = "/hpc/cuppen/shared_resources/HMF_data/DR-104/data/somatics/",
	cnvDir = "/hpc/cuppen/shared_resources/HMF_data/DR-104/data/somatics/",
	metadataHMF = "/hpc/cuppen/shared_resources/HMF_data/DR-104/metadata/metadata.tsv",
	expressionDir = "/hpc/cuppen/shared_resources/HMF_data/DR-104/data/isofix/",
	normalizedExpressionFile = "../data/expression/HMF_TMM.txt",
	causalGenesFile = "../data/genes/CCGC.tsv",
	nonCausalGenesFile = "../data/genes/hg19_proteinCodingGenes.bed",
	promoterFile = "../data/promoters/epdnew_hg38ToHg19_9vC8m.bed",
	cpgFile = "../data/cpg/cpgIslandExt.txt",
	tfFile = "../data/tf/tf_experimentallyValidated.bed_clustered.bed",
	chromHmmFile = "../data/chromhmm/hmec/GSE57498_HMEC_ChromHMM.bed",
	rankedGeneScoreDir = "linkedSVGenePairs",
	hg19CoordinatesFile = "../data/chromosomes/hg19Coordinates.txt",
	geneNameConversionFile = "../data/genes/allGenesAndIdsHg19.txt",
	tadFile = "../data/tads/hmec/HMEC_Lieberman-raw_TADs.bed",
	eQTLFile = "../data/eQTLs/hmec/hmec_eQTLs.bed_clustered.bed",
	enhancerFile = "../data/enhancers/hmec/hmec_encoderoadmap_elasticnet.117.txt",
	h3k4me3 = "../data/h3k4me3/hmec/ENCFF065TIH_h3k4me3.bed_clustered.bed",
	h3k27me3 = "../data/h3k27me3/hmec/ENCFF291WFP_h3k27me3.bed_clustered.bed",
	h3k27ac = "../data/h3k27ac/hmec/ENCFF154XFN_h3k27ac.bed_clustered.bed",
	h3k4me1 = "../data/h3k4me1/hmec/ENCFF336DDM_h3k4me1.bed_clustered.bed",
	dnaseIFile = "../data/dnase/hmec/ENCFF336OGZ.bed",
	rnaPolFile = "../data/rnapol/hmec/ENCFF433ZKP.bed",
	superEnhancerFile = "../data/superEnhancers/hmec/se_20200212_HMEC.bed",
	ctcfFile = "../data/ctcf/hmec/ENCFF288RFS.bed",
)