from kami import *

if __name__ == '__main__':
	data = load_table('data/out.txt', columns=['m', 'n', 'alpha'])
	print(list(lookup(4.5, 4.5, data)))
