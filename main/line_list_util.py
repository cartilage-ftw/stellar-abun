import pandas as pd
import numpy as np

"""
Manipulating line lists used by MOOG can be a pain. The format is weird
"""

# this name is used in the exported txt file names
star_name = 'sgr18532554'

# I usually write my measurements in a tsv file of some sort. The following should point to that file
# and read from it.
ew_meas_data = pd.read_csv('../data/sgr/sgr3700/wav_not_iron.txt', sep='\t')

# Then I have other MOOG-ready lists which are delimited by "whitespace" and contain gf values and everything
# 
line_list_path = '../data/sgr/sgr3700/sgr3700_line_list.txt'# Kirby's line list is '../data/HD122563.ew'

# use only the first 4 columns, I don't need the EW column
line_list_data = pd.read_csv(line_list_path, usecols=range(4), skiprows=1, delim_whitespace=True,
							names=['Wavelength', 'Ion', 'EP', 'log gf'])

def add_ew_meas(df):
	"""
	Add my EW measurements to the empty line list.
	"""
	# merge the EW column of my measurements to this line list
	df['EW'] = ew_meas_data['EW']


def clean_unknown_lines():
	# in the initial list Andy gave me, there were rows with gf values listed as 1.000
	# (these were not real values, rather "default" values assigned) when a proper gf value wasn't known for the line
	# TODO: avoid using global variables, instead, call it as a function param
	if line_list_data[3].dtype == float:
		line_data_with_gf = line_list_data[line_list_data[3] != 1.000]
	else:
		# if the number stayed as a string and didn't get coverted into a float
		line_data_with_gf = line_list_data[~line_list_data[3].isin(['1.000'])]
	print(f'orig: {len(line_list_data)}, clean: {len(line_data_with_gf)}')
	print(line_data_with_gf.head)


def add_empty_cols(data):
	"""
	A line list is actually supposed to have 6 columns
	"""
	# Usually, these two of these are kept blank for atomic species.
	cols = ['damping param', # van der Vaals damping parameter
	 		'D_0',] # dissociation energy for molecular features.
	for col in cols:
		data[col] = ['' for i in range(len(data))] # keep the whole column empty
	# and maybe, for EWs, put all nans
	data['EW'] = [np.nan for i in range(len(data))]
	print(data.head())


def export_whitespace_list(data, export_path, comment_heading):
	"""
	Cleaner script for exporting the data into a whitespace delimited script.
	"""
	ws_data = data.to_string(justify='right', col_space=10, header=False, index=False,
							na_rep='nan') # 'nan' is what MOOG likes to take as representation for NaN vals
	print(ws_data)
	with open(export_path, 'w') as export:
		export.write(comment_heading + '\n')
		export.write(ws_data)
		print(f'Exported {export} successfully.')


def export_finished_list(data, export_path, comment_heading):
	"""
	Note: this is an older script, I wrote a cleaner one. See export_whitespace_list()
	"""
	with open(export_path, 'w') as export:
		export.write(comment_heading + '\n')
		for i in range(len(data)):
			row = data.iloc[i]
			# each column consists of 10 characters (including spaces) justified towards the right
			export.write(f'{row[0]:.3f}'.rjust(10) + str(row[1]).rjust(10) + f'{row[2]:.3f}'.rjust(10)
						+ str(float(row[3])).rjust(10))
			# now, there are 2 columns that we're not including in our line lists, so for the final column
			# make it 30 characters justified to the right (the first 20 serve as empty columns)
			export.write(str(row['EW']).rjust(30))
			export.write('\n')


if __name__ == '__main__':
	add_empty_cols(line_list_data)
	#add_ew_meas(line_list_data)
	#line_list_data[0].to_csv('sgr3700_iron_lines.txt', sep='\t', header=False, index=False)
	# I used this one line to create a list of wavelengths and nothing else.
	#ew_meas_data['Wavelength'].to_csv('iron_line_list.txt', sep='\t', header=False, index=False)
	export_whitespace_list(line_list_data, f'{star_name}_line_list.txt',
				 comment_heading=f'{star_name} Spec EW Measurements')
