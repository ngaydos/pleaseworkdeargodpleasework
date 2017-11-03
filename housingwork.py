import csv
import numpy as np

zip_dict = {}
with open('EXTR_ResBldg.csv', 'rb') as csvfile:
	testreader = csv.reader(csvfile)
	skiptitle = False
	for row in testreader:
		zip_dict[(row[0], row[1])] = row[11]


with open('EXTR_RealPropApplHist_V.csv', 'rb') as csvfile:
	valchange = csv.reader(csvfile)
	headerrow = True
	datesdict = {}
	for row in valchange:
		if headerrow == True:
			headerrow = False
		elif (row[2] == '2017' and row[3] == 'R') or (row[2] == '2012' and row[3] == 'R'):
			if (row[0], row[1]) in datesdict:
				datesdict[(row[0], row[1])] += [(row[2],row[4])]
			else:
				datesdict[(row[0], row[1])] = [(row[2],row[4])]
		

valdict = {}

for key, value in datesdict.items():
	if len(value) == 2:
		if value[0][0] == '2017' and int(value[1][1]) != 0:
			valdict[key] = (int(value[0][1]) - int(value[1][1]))/float(value[1][1]) * 100
		elif value[0][0] == '2012' and int(value[0][1]) != 0:
			valdict[key] = (int(value[1][1]) - int(value[0][1]))/float(value[0][1]) * 100

from collections import defaultdict
zip_change = defaultdict(list)
avg_zip_change = {}
for mm in zip_dict:
	if mm in valdict:
		zip_change[zip_dict[mm]].append(valdict[mm])
for zipcode in zip_change:
	avg_zip_change[zipcode] = np.mean(zip_change[zipcode])
