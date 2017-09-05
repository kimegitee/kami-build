import numpy as np
import pandas as pd
import itertools

def load_table(filename: str, columns: list) -> pd.DataFrame:
	'''Turn a look up table with values as column names to a table with
	multiple primary keys. Example:

	Original table:
         1    2
	1    0    0
	2    0    0

	Normalized table:

	col1 col2 col3
	1    1    0
	1    2    0
	2    1    0
	2    2    0
	----------------	
	args:
		filename: str file location. File must be csv.
		columns: list of str. List of column names.
	returns:
		pandas.DataFrame
	'''
	assert len(columns) == 3, 'Must supply exactly 3 columns'
	data = np.genfromtxt(filename, dtype='float64', delimiter=',')
	col1 = data[1:, 0]
	col2 = data[0, 1:]
	col3 = data[1:, 1:].reshape(-1, 1)
	index = np.array(list(itertools.product(col1, col2)))
	data = np.concatenate([index, col3], 1)
	# Don't use float as index
	data = pd.DataFrame(data, columns=columns)

	return data

def find_next(value: float, data: pd.Series) -> (float, float):
	'''Find nearest smaller and bigger values of value'''
	assert type(data) is pd.Series,\
		'Expecting a pandas Series, got {} instead'.format(type(data))
	prev_value = data[data <= value].max()
	next_value = data[data >= value].min()
	
	return prev_value, next_value

def lookup(val1: float, val2: float, data: pd.DataFrame):
	'''Look up nearest values to v1 and v2 from data'''
	col1 = data.iloc[:, 0]
	col2 = data.iloc[:, 1]
	for next_val1 in find_next(val1, col1):
		for next_val2 in find_next(val2, col2):
			result = data[(col1 == next_val1) & (col2 == next_val2)].iloc[0, 2]
			yield col1, col2, result