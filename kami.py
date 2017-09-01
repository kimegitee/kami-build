import numpy as np
import pandas as pd

def load_table(filename: str, columns: list):
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
	data = np.genfromtxt(filename, delimiter=',')
	col1 = data[1:, 0]
	col2 = data[0, 1:]
	col3 = data[1:, 1:].reshape(-1)
	index = pd.MultiIndex.from_product([col1, col2], names=columns[:-1])
	data = pd.DataFrame(col3, index, columns[-1:])

	return data

if __name__ == '__main__':
	data = load_table('data/out.txt', columns=['m', 'n', 'alpha'])
	print(data)
