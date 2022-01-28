import seaborn as sns

from plot_moog_abun import *

"""
I was testing if some lines showed signs of blends. I thought they'd show up if I did only EW measurements
Tbh, the real way is doing spec synthesis.
"""

sgr_path = '../data/sgr/'
coI_outfile = '/blends/coI/coI.out2'
mnI_outfile = '/blends/mn/mnI.out2'

sgr3700_coI = read_element_abun(sgr_path + 'sgr3700' + coI_outfile,
		 element='Co I', drop_nan=True)
sgr4210_coI = read_element_abun(sgr_path + 'sgr4210' + coI_outfile,
		 element='Co I', drop_nan=True)

# sgr3700aper51 contains 6630 to 6823 A
#sgr370

#print(sgr3700_coI)

def plot_abuns(data_list, solar_val, metal_list, element='Co I'):
	co_fig, co_ax = plt.subplots(figsize=(6,6))
	for data, metal in zip(data_list, metal_list):
		datum = data[data['abund'] < 999.0]
		abunds = np.array(tuple(datum['abund']))
		datum['brac_abund'] = abunds - solar_val - metal
		#print(datum)
		sns.scatterplot(data=datum, x='wavelength', y='brac_abund', label=f'[Fe/H]={metal}')

		print(f"Average [{element}/Fe] = {np.average(datum['brac_abund']):0.2f}."
		 + f" Sigma = {np.std(datum['brac_abund']):0.2f}\n"
		+ f" for star with [Fe/H] = {metal}")
	co_ax.vlines(x=list(datum['wavelength']), ymin = -1, ymax=0, color='gray', lw=1)
	plt.ylabel(f'[{element}/Fe]')

co_sun = 4.94
plot_abuns([sgr3700_coI, sgr4210_coI], solar_val=co_sun, metal_list=[-0.88, -0.17])

sgr3700_mnI = read_element_abun(sgr_path + 'sgr3700' + mnI_outfile,
				element='Mn I', drop_nan=True)
sgr4210_mnI = read_element_abun(sgr_path + 'sgr4210' + mnI_outfile,
				element='Mn I', drop_nan=True)

plot_abuns([sgr3700_mnI, sgr4210_mnI], solar_val = 5.42, metal_list=[-0.88, -0.17], element='Mn')

plt.show()