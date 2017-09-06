from kami import *
from flask import Flask

if __name__ == '__main__':
	data = load_table('data/out.txt', columns=['m', 'n', 'alpha'])
	print(list(lookup(52, 45, data)))
