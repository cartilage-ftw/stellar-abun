import pandas as pd
import matplotlib.pyplot as plt

"""
Script for plotting data from abundance output summary file from MOOG.
"""


def read_element_abun(file_path, element='Fe I'):
	"""
	Reads the abundancy summary output file by MOOG, searches for a specific element's abundance
	in it, and returns it into a pandas DataFrame
	"""
	# wait until you hit this
	text_to_start = 'Abundance Results for Species ' + element + ' ' # the extra ' ' ensures Fe II doesn't get matched
	# stop reading once you hit this.
	text_to_stop = 'average abundance'
	start = stop = -1
	with open(file_path) as summary_file:
		lines = summary_file.readlines()
		for i in range(len(lines)):
			# start reading once you encounter that
			if text_to_start in lines[i]:
				start = i+1
				continue
			if text_to_stop in lines[i]:
				stop = i-1
				break
		num_rows = stop - start
	print('Stop at', stop)
	return pd.read_csv(file_path, delim_whitespace=True, skiprows=start, nrows=num_rows)


def plot_element_abun(data):
	"""
	Plot abundance (vertical axis) vs EP and other stuff.
	"""
	fig, axes = plt.subplots(figsize=(10, 5), nrows=1, ncols=2, sharey=True)
	axes[0].plot(data['EP'], data['abund'], 'mo', markersize=3)
	axes[0].set_xlabel('Excitation Potential $(\chi)$')
	axes[0].set_ylabel('[Fe I/H]')
	axes[1].plot(data['EWin'], data['abund'], color='olive', linestyle='', marker='o', markersize=3)
	axes[1].set_xlabel('Equivalent Width')
	plt.subplots_adjust(hspace=0, wspace=0)
	plt.show()


if __name__ == '__main__':
	abun_data = read_element_abun('../data/arcturus/elements/arcturus.out2')
	plot_element_abun(abun_data)
