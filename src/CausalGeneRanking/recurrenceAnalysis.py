"""

	This script serves to do recurrence analysis on the sv-gene pairs identified
	
	The following information is useful to report on:
	- In the positive SV-gene pairs, how many are recurrently found across patients?
	- What is the distribution of recurrent genes across SV types?

"""

import sys
import numpy as np
import random
from scipy import stats
from statsmodels.sandbox.stats.multicomp import multipletests
import matplotlib.pyplot as plt


#load the sv-gene pairs
positivePairs = np.loadtxt(sys.argv[1], dtype='object')
print(positivePairs.shape)

degPairs = np.loadtxt(sys.argv[2], dtype='object')

#format: gene as key, as values, the first is the number of times we found the gene,
#the second how many were dels, then dups, invs, itx.
splitPairs = dict()
genes = dict()
for pair in positivePairs:
	splitPair = pair[0].split('_')

	if splitPair[0] + '_' + splitPair[7] not in splitPairs:
		splitPairs[splitPair[0] + '_' + splitPair[7]] = []
	splitPairs[splitPair[0] + '_' + splitPair[7]].append(pair)

	if splitPair[0] not in genes:
		
		#count, cross-patient count, nc: del, dup, inv, itx, snv, cnv amp, cnv del, sv del, sv dup, sv inv, sv itx
		genes[splitPair[0]] = [0]*13
		genes[splitPair[0]].append([]) #add the patient names here

	genes[splitPair[0]][0] += 1
	
	if splitPair[12] == 'DEL':
		genes[splitPair[0]][1] += 1
	elif splitPair[12] == 'DUP':
		genes[splitPair[0]][2] += 1
	elif splitPair[12] == 'INV':
		genes[splitPair[0]][3] += 1
	elif splitPair[12] == 'ITX':
		genes[splitPair[0]][4] += 1

	patient = splitPair[7]
	genes[splitPair[0]][13].append(patient)
	
	
#convert to numpy array for easy ranking
recurrentGenes = []
for gene in genes:

	#count how many unique patients affect the gene for recurrence
	uniquePatients = np.unique(genes[gene][13])
	
	data = [gene] + [len(uniquePatients)] + genes[gene]
	
	recurrentGenes.append(data)

recurrentGenes = np.array(recurrentGenes, dtype='object')

#sort
sortedGenes = recurrentGenes[np.argsort(recurrentGenes[:,1])[::-1]]

#make random distribution
negativeCounts = []
for ind in range(0, 100):
	
	#randomly sample any gene from the positive set.
	#then count how often we find that gene.
	randInd = random.sample(range(0, positivePairs.shape[0]), 1)
	
	randomPair = positivePairs[randInd][0]
	
	splitPair = randomPair[0].split('_')
	
	gene = splitPair[0]
	#check how often we find this gene
	recurrenceCount = sortedGenes[np.where(sortedGenes[:,0] == gene)[0],1][0]
	
	negativeCounts.append(recurrenceCount)
	
#do t-test for each gene against this random set
pValues = []
for gene in sortedGenes:
	
	z = gene[1] - np.mean(negativeCounts) / float(np.std(negativeCounts))

	pValue = stats.norm.sf(abs(z))*2
	pValues.append(pValue)

#do MTC on the p-values
reject, pAdjusted, _, _ = multipletests(pValues, method='bonferroni')

ind = 0
for rejectVal in reject:
	
	if rejectVal == True:
		print(sortedGenes[ind])

	ind += 1

#make a matrix in which we show visually which genes are affected in which patients
#this matrix is genes x patients
uniquePatients = dict()
top = 15 #making the matrix only for the top X genes
ind = 0
for gene in sortedGenes:
	
	if ind >= top:
		continue
	
	patients = gene[15]
	for patient in patients:
		if patient not in uniquePatients:
			uniquePatients[patient] = 0
		uniquePatients[patient] += 1

	ind += 1

#make a matrix of genes by patients
recurrenceMatrix = np.zeros([top, len(uniquePatients)])
ind = 0
patientOrder = dict() #order of patients in the matrix

for patientInd in range(0, len(uniquePatients)):
	
	patient = list(uniquePatients.keys())[patientInd]
	
	patientOrder[patient] = patientInd
	
for gene in sortedGenes:
	
	if ind >= top:
		continue
	
	patients = gene[15]
	for patient in patients:
		
		patientInd = patientOrder[patient]
		recurrenceMatrix[ind, patientInd] += 1
		
	ind += 1	
		
print(recurrenceMatrix)

#make a grid plot, showing the different SV types that the patients have
#color the genes with -/+ direction, see if it correlates with the SV types.
fig, ax = plt.subplots()
for row in range(0, recurrenceMatrix.shape[0]):
	
	if row < recurrenceMatrix.shape[0]-1:
		ax.axhline(row+0.5, linestyle='--', color='k', linewidth=0.5)
	
	for col in range(0, recurrenceMatrix.shape[1]):
		
		if col < recurrenceMatrix.shape[1]-1:
			ax.axvline(col+0.5, linestyle='--', color='k', linewidth=0.5)
		
		if recurrenceMatrix[row,col] > 0:
			
			#get the sv type to see which symbol to assign
			gene = sortedGenes[row, 0]
			patient = list(uniquePatients.keys())[col]
			
			pairs = splitPairs[gene + '_' + patient]
			
			#generate some random offsets to avoid overlapping data
			offsetsX = random.sample(range(-30,30), len(pairs))
			offsetsX = [i / float(100) for i in offsetsX]
			
			offsetsY = random.sample(range(-30,30), len(pairs))
			offsetsY = [i / float(100) for i in offsetsY]
							
			ind = 0
			for pair in pairs:
				
				splitPair = pair[0].split('_')
				svType = splitPair[12]
			
				markerType = '.'
				if svType == 'DEL':
					markerType = '.'
				elif svType == 'DUP':
					markerType = 's'
				elif svType == 'INV':
					markerType = '^'
				elif svType == 'ITX':
					markerType = '*'
					
				#also get up/down color
				if patient + '_' + gene in degPairs[:,0]: 
					
					#get the z-score of the pair. 
					degPairInfo = degPairs[degPairs[:,0] == patient + '_' + gene][0]
		
					color = 'red'
					if float(degPairInfo[5]) > 1.5:
						color = 'red'
					elif float(degPairInfo[5]) < -1.5:
						color = 'blue'
					else:
						print('this should never happen')
				
				plt.scatter(col + offsetsY[ind], offsetsX[ind] + (recurrenceMatrix.shape[0] - row -1), marker=markerType, edgecolor=color,
							facecolor='none', s=35)
				ind += 1
#the genes are swapped around to show the most recurrent on top, so reverse thelabels as well
plt.yticks(range(0, recurrenceMatrix.shape[0]), sortedGenes[0:top,0][::-1])
plt.xticks(range(0, recurrenceMatrix.shape[1]), list(uniquePatients.keys()), rotation=90)
#plt.grid()
plt.tight_layout()
plt.show()
exit()
plt.clf()

		
	
	

	
#Next, we are interested in patients with alternative mutations.
#So here, for each gene, first show how many patients have an SNV, CNV, or SV
#keep in mind that a duplication could be non-coding if it is in the same patient
#this will later become obvious in the visualization

#load the patient-gene mutation pairs
snvPatients = np.load('snvPatients.npy', allow_pickle=True, encoding='latin1').item()

svPatientsDel = np.load('svPatientsDel.npy', allow_pickle=True, encoding='latin1').item()
svPatientsDup = np.load('svPatientsDup.npy', allow_pickle=True, encoding='latin1').item()
svPatientsInv = np.load('svPatientsInv.npy', allow_pickle=True, encoding='latin1').item()
svPatientsItx = np.load('svPatientsItx.npy', allow_pickle=True, encoding='latin1').item()

cnvPatientsDel = np.load('cnvPatientsDel.npy', allow_pickle=True, encoding='latin1').item()
cnvPatientsAmp = np.load('cnvPatientsAmp.npy', allow_pickle=True, encoding='latin1').item()

for pair in positivePairs:
	
	splitPair = pair[0].split('_')
	
	gene = splitPair[0]
	patient = splitPair[7]
	
	sortedGeneInd = np.where(sortedGenes[:,0] == gene)[0]
	
	if gene in snvPatients[patient]:
		sortedGenes[sortedGeneInd, 5] += 1
	if gene in cnvPatientsDel[patient]:
		sortedGenes[sortedGeneInd, 6] += 1
	if gene in cnvPatientsAmp[patient]:
		sortedGenes[sortedGeneInd, 7] += 1
	if gene in svPatientsDel[patient]:
		sortedGenes[sortedGeneInd, 8] += 1	
	if gene in svPatientsDup[patient]:
		sortedGenes[sortedGeneInd, 9] += 1
	if gene in svPatientsInv[patient]:
		sortedGenes[sortedGeneInd, 10] += 1
	if gene in svPatientsItx[patient]:
		sortedGenes[sortedGeneInd, 11] += 1	
	
print(sortedGenes[0:15,:])

#show these data in a bar plot.
#for each type of mutation, add to the stacked bar chart.
#fig,ax = plt.subplots()
geneInd = 0
ymax = 0
for gene in sortedGenes[0:15]:
	
	plt.bar(geneInd, gene[5], color='yellow')
	plt.bar(geneInd, gene[6], bottom=gene[5], color='cyan')
	plt.bar(geneInd, gene[7], bottom=gene[5]+gene[6], color='green')
	plt.bar(geneInd, gene[8], bottom=gene[5]+gene[6]+gene[7], color='red')
	plt.bar(geneInd, gene[9], bottom=gene[5]+gene[6]+gene[7]+gene[8], color='orange')
	plt.bar(geneInd, gene[10], bottom=gene[5]+gene[6]+gene[7]+gene[8]+gene[9], color='magenta')
	plt.bar(geneInd, gene[11], bottom=gene[5]+gene[6]+gene[7]+gene[8]+gene[9]+gene[10], color='black')
	
	if gene[5]+gene[6]+gene[7]+gene[8]+gene[9]+gene[10]+gene[11] > ymax:
		ymax = gene[5]+gene[6]+gene[7]+gene[8]+gene[9]+gene[10]+gene[11]
	
	geneInd += 1

#this doesn't fit for some reason
plt.ylim(0,ymax+1)
plt.tight_layout()	
plt.show()


