                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                s='auto', max_depth=80, bootstrap=True)
	else:
		print('Please provide a valid SV type')
		exit(1)


	#divide into chromosomes.

	positivePairsPerChromosome = dict()
	for pair in normalizedPositivePairs:

		splitPair = pair[0].split('_')

		if splitPair[12] != svType:
			continue

		if splitPair[1] not in positivePairsPerChromosome:
			positivePairsPerChromosome[splitPair[1]] = []

		allFeatures = []
		for featureInd in range(1, len(pair)):

			if featureInd in allowedFeatures:
				allFeatures.append(pair[featureInd])

		positivePairsPerChromosome[splitPair[1]].append(allFeatures)


	negativePairsPerChromosome = dict()
	matchPairsNeg = 0
	for pair in normalizedNegativePairs:

		splitPair = pair[0].split('_')

		if splitPair[12] != svType:
			continue

		if splitPair[1] not in negativePairsPerChromosome:
			negativePairsPerChromosome[splitPair[1]] = []

		allFeatures = []
		for featureInd in range(1, len(pair)):

			#if featureInd-1 in badIdx: #skip 0 variance
			#	continue

			if featureInd in allowedFeatures:
				allFeatures.append(pair[featureInd])

		negativePairsPerChromosome[splitPair[1]].append(allFeatures)

	chromosomes = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7',
				   'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13',
				   'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
				   'chr20', 'chr21', 'chr22']



	#go through the chromosomes and make the positive/negative sets
	#subsample the negative set to the same size.
	aucs = []
	#for the test set, keep statistics for TPR and FPR to compare between methods
	totalTP = 0
	totalFP = 0
	totalTN = 0
	totalFN = 0
	totalP = 0
	totalN = 0
	for chromosome in chromosomes:

		if chromosome not in positivePairsPerChromosome or chromosome not in negativePairsPerChromosome:
			continue

		testPositivePairs = np.array(positivePairsPerChromosome[chromosome])
		testNegativePairs = np.array(negativePairsPerChromosome[chromosome])

		#randomly subsample
		randInd = random.sample(range(0, testNegativePairs.shape[0]), testPositivePairs.shape[0])
		testNegativeSubset = testNegativePairs[randInd]

		testSet = np.concatenate((testPositivePairs, testNegativeSubset))
		testLabels = [1]*testPositivePairs.shape[0] + [0]*testNegativeSubset.shape[0]

		totalP += testPositivePairs.shape[0]
		totalN += testNegativeSubset.shape[0]

		trainingSet = []
		trainingLabels = []
		for chromosome2 in positivePairsPerChromosome:

			if chromosome2 == chromosome:
				continue

			if chromosome2 not in positivePairsPerChromosome or chromosome2 not in negativePairsPerChromosome:
				continue

			chrPositivePairs = np.array(positivePairsPerChromosome[chromosome2])
			chrNegativePairs = np.array(negativePairsPerChromosome[chromosome2])

			#randomly subsample
			randInd = random.sample(range(0, chrNegativePairs.shape[0]), chrPositivePairs.shape[0])
			chrNegativeSubset = chrNegativePairs[randInd]

			#chrTrainingSet = np.concatenate((chrPositivePairs, chrNegativeSubset))

			#trainingSet.append(list(chrTrainingSet))

			for pair in chrPositivePairs:
				trainingSet.append(pair)
			for pair in chrNegativeSubset:
				trainingSet.append(pair)

			chrLabels = [1]*chrPositivePairs.shape[0] + [0]*chrNegativeSubset.shape[0]
			trainingLabels += chrLabels

		trainingSet = np.array(trainingSet)

		allPairs = np.concatenate((trainingSet, testSet))
		from sklearn.feature_selection import VarianceThreshold
		t = 0
		vt = VarianceThreshold(threshold=t)
		vt.fit(allPairs)
		idx = np.where(vt.variances_ > t)[0]
		badIdx = np.where(vt.variances_ <= t)[0]

		trainingSet = trainingSet[:,idx]
		testSet = testSet[:,idx]

		classifier.fit(trainingSet, trainingLabels)

		#check true/false positives/negatives
		predictions = classifier.predict(testSet)
		for labelInd in range(0, len(testLabels)):

			if testLabels[labelInd] == 1 and predictions[labelInd] == 1:
				totalTP += 1
			elif testLabels[labelInd] == 0 and predictions[labelInd] == 1:
				totalFP += 1
			elif testLabels[labelInd] == 1 and predictions[labelInd] == 0:
				totalFN += 1
			else:
				totalTN += 1

		fig, ax = plt.subplots()
		viz = plot_roc                                                                                                                                                                                                                                                                                                                                                                                                       