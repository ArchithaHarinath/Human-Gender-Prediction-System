import csv
from math import exp

#data loading of traing set and test set
def readdata(filename):
	trainingset=list()
	file=open(filename, "r")
	csv_reader=csv.reader(file)
	for row in csv_reader:
		if not row:
			continue
		trainingset.append(row)
	return trainingset
#labelling of men data as 1 and women data as 0
def dataconvertor(trainingset):
	labels={}
	i=float(0)
	for data in trainingset:
		cat_data=data[-1]
		if cat_data not in labels:
			labels[cat_data]=i
			data[-1]=i  
			i=i+1
		else:
			data[-1]=labels[data[-1]]
	return trainingset
	
#convert the data points from string value to float
def tofloat(trainingset,hasClassColumn):
	for i in range(len(trainingset[0])-hasClassColumn):
		for row in trainingset:
			row[i]=float(row[i].strip())
	return trainingset

#normalization of data points by subtracting the minimum and the maximum values from the dataset
def normalization(trainingset,minmax):
	for row in trainingset:
		for i in range(len(row)):
			row[i]=(row[i]-minmax[i][0])/(minmax[i][1]-minmax[i][0])
	return trainingset

#prediction of the values
def resultprediction(row,coefficients):
	x=coefficients[0]
	for i in range(len(row)-1):
		x+=coefficients[i+1]*row[i]
	return 1.0/(1.0+exp(-x))

#theta values
def coefficientvalues(train,alpha,itr):	
	coef=[0.0 for i in range(len(train[0]))]
	for epoch in range(itr):
		for row in train:	
			prediction=resultprediction(row, coef)
			error=row[-1]-prediction
			coef[0]=coef[0]+alpha*error*prediction*(1.0-prediction)
			for i in range(len(row)-1):
				coef[i+1]=coef[i+1]+alpha*error*prediction*(1.0-prediction)*row[i]
	print(coef)
	return coef
 
	
def main():
	#load the data points for training set and test set
	filename=input("Input the filename of the trainingset data: ")
	trainingset=readdata(filename)
	trainingset=dataconvertor(trainingset)
	trainingset=tofloat(trainingset,hasClassColumn=True)
	filename=input("Input the filename of the testset data: ")
	test_set=readdata(filename)
	testset=tofloat(test_set,hasClassColumn=False)
	#calculate minimum and maximum values
	minmax=[]
	for x in range(len(trainingset[0])):
		col_values=[y[x] for y in trainingset]
		value_min=min(col_values)
		value_max=max(col_values)
		minmax.append([value_min, value_max])	
	trainingset=normalization(trainingset, minmax)
	testset=normalization(testset, minmax)
	alpha=0.05
	itr=100
	coef=coefficientvalues(trainingset, alpha, itr)
	#result set prediction
	result =[]
	for x in testset:
		temp=resultprediction(x, coef)
		result.append(round(temp))
	for i in range (len(result)):
		if(result[i]==0):
			print("The test set "+str(i)+" belongs to class W")
		else:
			print("The test set "+str(i)+" belongs to class M")
			
main()