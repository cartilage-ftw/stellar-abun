import pandas as pd

pd.options.display.max_rows = None

dat = pd.read_fwf("../../data/mystery/47_tuc_8_data/47tuc_ews.dat", delim_whitespace=True, skiprows=[1])
# drop rows with nan values in ' EW(8)'
dat.dropna()
for i in range(len(dat)):
	if 'Fe  I' in dat['#Ion '].iloc[i]:
		print(str(dat[' Wav(A)'].iloc[i]) + '\t' + str(dat[' EW(8)'].iloc[i]))
print(dat.columns)