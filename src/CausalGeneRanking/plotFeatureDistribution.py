"""
	Make feature distribution plots for the somatic and germline SVs. Boxplots for gains and losses separate.

"""

import numpy as np
import sys
import matplotlib.pyplot as plt

scores = np.loadtxt(sys.argv[1], dtype="object")

eQTLLosses = scores[:,5].astype(float)
enhancerLosses = scores[:,7].astype(float)
promoterLosses = scores[:,9].astype(float)
cpgLosses = scores[:,11].astype(float)
tfLosses = scores[:,13].astype(float)
hicLosses = scores[:,15].astype(float)
h3k9me3Losses = scores[:,17].astype(float)
h3k4me3Losses = scores[:,19].astype(float)
h3k27acLosses = scores[:,21].astype(float)
h3k27me3Losses = scores[:,23].astype(float)
h3k4me1Losses = scores[:,25].astype(float)
h3k36me3Losses = scores[:,27].astype(float)
dnaseLosses = scores[:,29].astype(float)

lossData = [eQTLLosses, enhancerLosses, promoterLosses, cpgLosses, tfLosses, hicLosses, h3k9me3Losses, h3k4me3Losses, h3k27acLosses, h3k27me3Losses, h3k4me1Losses, h3k36me3Losses, dnaseLosses]

# filteredLossData = []
# for dataset in lossData:
# 	filteredDataset = []
# 	for value in dataset:
# 		
# 		if value > 0:
# 			print value
# 			filteredDataset.append(value)
# 	print filteredDataset
# 	exit()
# 	filteredLossData.append(filteredDataset)

#make boxplot for losses

# Create the boxplot
fig, ax = plt.subplots()
bp = plt.boxplot(lossData)
ax.set_xticklabels(['eQTLs', 'enhancers', 'promoters', 'CpG', 'TF', 'HiC', 'h3k9me3', 'h3k4me3', 'h3k27ac', 'h3k27me3', 'h3k4me1', 'h3k36me3', 'DNAseI'])
plt.xticks(rotation=70)
# Save the figure
plt.savefig("losses_germline.png", bbox_inches='tight')


#Repeat but then for gains


eQTLGains = scores[:,4].astype(float)
enhancerGains = scores[:,6].astype(float)
promoterGains = scores[:,8].astype(float)
cpgGains = scores[:,10].astype(float)
tfGains = scores[:,12].astype(float)
hicGains = scores[:,14].astype(float)
h3k9me3Gains = scores[:,16].astype(float)
h3k4me3Gains = scores[:,18].astype(float)
h3k27acGains = scores[:,20].astype(float)
h3k27me3Gains = scores[:,22].astype(float)
h3k4me1Gains = scores[:,24].astype(float)
h3k36me3Gains = scores[:,26].astype(float)
dnaseGains = scores[:,28].astype(float)

gainData = [eQTLGains, enhancerGains, promoterGains, cpgGains, tfGains, hicGains, h3k9me3Gains, h3k4me3Gains, h3k27acGains, h3k27me3Gains, h3k4me1Gains, h3k36me3Gains, dnaseGains]



fig, ax = plt.subplots()
bp = plt.boxplot(gainData)
ax.set_xticklabels(['eQTLs', 'enhancers', 'promoters', 'CpG', 'TF', 'HiC', 'h3k9me3', 'h3k4me3', 'h3k27ac', 'h3k27me3', 'h3k4me1', 'h3k36me3', 'DNAseI'])
plt.xticks(rotation=70)
# Save the figure
plt.savefig("gains_germline.png", bbox_inches='tight')



