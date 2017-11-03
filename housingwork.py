import csv
import numpy as np

def top50zips(zipdata, valuedata):
	zip_dict = createzipdict(zipdata)
	value_dict = createvaluedict(valuedata)
	avg_zip_change = valuechange_by_zip(zip_dict, value_dict)
	#sort the zip codes by the average change value
	list(sorted(avg_zip_change.items(), key = lambda x : x[1]))
	L = len(avg_zip_change)
	return avg_zip_change[(L+1)/2 :]


def createzipdict(filename):
	zip_dict = {}
	with open(filename, 'rb') as csvfile:
		testreader = csv.reader(csvfile)
		skiptitle = False
		for row in testreader:
			if len(row[11][0:5]) == 5:
				zip_dict[(row[0], row[1])] = row[11][0:5]
	return zip_dict


def createvaluedict(filename):
	with open(filename, 'rb') as csvfile:
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
	return valdict


def valuechange_by_zip(zip_dict, valdict):
    """
    Arguments
    ---------
    zip_dict : dictionary with
               (Major, Minor) : zip code
    value_dict : dictionary with
                 (Major, Minor) : percent change in value between 2012 and 2017

    Output
    --------
    avg_zip_change : dictionary with
                     zip : average percent change in value between 2012 and 2017
                           within the region
    """
	from collections import defaultdict
	zip_change = defaultdict(list)
	avg_zip_change = {}
	for mm in zip_dict:
		if mm in valdict:
			zip_change[zip_dict[mm]].append(valdict[mm])
	for zipcode in zip_change:
		avg_zip_change[zipcode] = np.mean(zip_change[zipcode])
	return avg_zip_change

