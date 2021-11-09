#import dependencies
import pandas as pd
import numpy as np

#Read in data file or query
transformed_data_df = pd.read_csv('#path to file here.csv')


#create new column named 'Gram Type' and determine by species which are labeled Gram Positive or Gram Negative
#start by creating a list of Gram Positive species names 
species = ['Staphylococcus','Streptococcus', 'Enterococcus', 'Candida', 'Corynebacterium', 'Lactobacillus', 'Rothia', 
'Coryneform', 'Granulicatella', 'Positive', 'Cryptococcus', 'Listeria', 'Lactococcus', 'Dermabacter', 'Mycobacterium', 'Gemella',
'Cutibacterium', 'Yeast', 'Lactobacillus', 'Actinomyces', 'Kocuria', 'Alloiococcus', 'Actinomyces', 'Rhodotorula', 'Trueperella', 'Aerococcus', 
'Kodameae', 'Leuconostoc', 'Microbacterium', 'Facklamia', 'Bifidobacterium', 'Strep', 'Micrococcus', 'Rhodococcus', 'Rothia', 'Gardernella',
'Nocardia', 'Gordonia', 'Tricosporon', 'Trichosporon', 'Cryptococcus']

#If species is in the list above, then call 'Gram Positive' and by default all others are called 'Gram Negative'
transformed_data_df["Gram Type"] = transformed_data_df["Organism"].str.contains('|'.join(species), na=False)
transformed_data_df["Gram Type"] = transformed_data_df["Gram Type"].replace({True: 'Gram Positive', False: 'Gram Negative'})


#define ESBL condition and create new column 'ESBL'
def esbl(s):
    if (s['Gram Type'] == 'Gram Negative') and ((s['Ceftriaxone R'] == 'Resistant') or (s['Ceftazidime R'] == 'Resistant') or (s['Cefotaxime R'] == 'Resistant') 
    or (s['Cefepime R'] == 'Resistant')):
        return '1'
    else:
        return '0'

transformed_data_df['ESBL'] = transformed_data_df.apply(esbl, axis=1)


#define FQ condition and create new column 'FQ'
transformed_data_df["Bacillus"] = transformed_data_df["Organism"].str.contains('Bacillus', na=False)

def fq(s):
    if (s['Bacillus'] ==True and s['Gram Type'] == 'Gram Negative') and ((s['Ciprofloxacin R'] == 'Resistant') or (s['Levofloxacin R'] == 'Resistant')
    or (s['Moxifloxacin R'] == 'Resistant') or (s['Ciprofloxacin R'] == 'Intermediate') or (s['Levofloxacin R'] == 'Intermediate') or (s['Moxifloxacin R'] == 'Intermediate')):
        return '1'
    else:
        return '0'

transformed_data_df['FQ'] = transformed_data_df.apply(fq, axis=1)
del transformed_data_df['Bacillus']

#create list of enterobacter species
enterobacter_list = ['Klebsiella', 'Escherichia', 'Citrobacter', 'Enterobacter', 'Enterobacillus', 'Raoultella', 'Shigella', 'Salmonella']

#create new column named 'Enterobacter' and determine by organism TRUE or FALSE
transformed_data_df["Enterobacter"] = transformed_data_df["Organism"].str.contains('|'.join(enterobacter_list), na=False)


#define CRE condition and create new column 'CRE'
def CRE(s):
    if (s['Enterobacter'] ==True) and ((s['Ertapenem R'] == 'Resistant') or (s['Imipenem R'] == 'Resistant') or (s['Meropenem R'] == 'Resistant') 
    or (s['Ertapenem R'] == 'Intermediate') or (s['Imipenem R'] == 'Intermediate') or (s['Meropenem R'] == 'Intermediate')):
        return '1'
    else:
        return '0'

transformed_data_df['CRE'] = transformed_data_df.apply(CRE, axis=1)
del transformed_data_df['Enterobacter']

#create new column named 'Acinetobacter' and determine by organism TRUE or FALSE
transformed_data_df["Acinetobacter"] = transformed_data_df["Organism"].str.contains('Acinetobacter', na=False)

#define CRA (Carbapenem Resistant Acinetobacter) condition and create new column 'CRA'
def CRA(s):
    if (s['Acinetobacter'] ==True) and ((s['Ertapenem R'] == 'Resistant') or (s['Imipenem R'] == 'Resistant') or (s['Meropenem R'] == 'Resistant') 
    or (s['Ertapenem R'] == 'Intermediate') or (s['Imipenem R'] == 'Intermediate') or (s['Meropenem R'] == 'Intermediate')):
        return '1'
    else:
        return '0'

transformed_data_df['CRA'] = transformed_data_df.apply(CRA, axis=1)
del transformed_data_df['Acinetobacter']

#create new column named 'Enterococcus' and determine by organism TRUE or FALSE
transformed_data_df["Enterococcus"] = transformed_data_df["Organism"].str.contains('Enterococcus', na=False)

#define VRE, LRE, and Daptomycin-NS conditions based off of new 'Enterococcus column' and create columns 'VRE', 'LRE', 'Daptomycin-NS'
def VRE(s):
    if (s['Enterococcus'] ==True) and ((s['Vancomycin R'] == 'Resistant') or (s['Vancomycin R'] == 'Intermediate')):
        return '1'
    else:
        return '0'

transformed_data_df['VRE'] = transformed_data_df.apply(VRE, axis=1)

def LRE(s):
    if (s['Enterococcus'] ==True) and ((s['Linezolid R'] == 'Resistant') or (s['Linezolid R'] == 'Intermediate')):
        return '1'
    else:
        return '0'

transformed_data_df['LRE'] = transformed_data_df.apply(LRE, axis=1)

def Daptomycin_NS(s):
    if (s['Enterococcus'] ==True) and (s['Daptomycin R'] == 'Non Susceptible'):
        return '1'
    else:
        return '0'

transformed_data_df['Daptomycin_NS'] = transformed_data_df.apply(Daptomycin_NS, axis=1)
del transformed_data_df['Enterococcus']

#create new column named 's_aureus' and determine by organism TRUE or FALSE
transformed_data_df["s_aureus"] = transformed_data_df["Organism"].str.contains('Staphylococcus aureus', na=False)

#define MRSA, MSSA, VISA and VRSA based off of new 'Staphylococcus column, create new columns 'MRSA', 'MSSA', 'VISA', and 'VRSA'
def MRSA(s):
    if (s['s_aureus'] ==True) and (s['Oxacillin R'] == 'Resistant'):
        return '1'
    else:
        return '0'

transformed_data_df['MRSA'] = transformed_data_df.apply(MRSA, axis=1)

def MSSA(s):
    if (s['s_aureus'] ==True) and (s['Oxacillin R'] == 'Susceptible'):
        return '1'
    else:
        return '0'

transformed_data_df['MSSA'] = transformed_data_df.apply(MSSA, axis=1)

def VISA(s):
    if (s['s_aureus'] ==True) and (s['Linezolid R'] == 'Intermediate'):
        return '1'
    else:
        return '0'

transformed_data_df['VISA'] = transformed_data_df.apply(VISA, axis=1)

def VRSA(s):
    if (s['s_aureus'] ==True) and (s['Linezolid R'] == 'Resistant'):
        return '1'
    else:
        return '0'

transformed_data_df['VRSA'] = transformed_data_df.apply(VRSA, axis=1)
del transformed_data_df['s_aureus']

#create new column named 'Candida' and determine by organism TRUE or FALSE
transformed_data_df["Candida"] = transformed_data_df["Organism"].str.contains('Candida', na=False)

#define FRC (Fluconazole Resistant Candida) conditions based off of new 'Candida' and create new column 'FRC'
def FRC(s):
    if (s['Candida'] ==True) and (s['Fluconazole R'] == 'Resistant'):
        return '1'
    else:
        return '0'

transformed_data_df['FRC'] = transformed_data_df.apply(FRC, axis=1)
del transformed_data_df['Candida']

#create new column named 'Pseudomonas' and determine by organism TRUE or FALSE
transformed_data_df["Pseudomonas"] = transformed_data_df["Organism"].str.contains('Pseudomonas', na=False)

#define CRP (Carbapenem Resistant Pseudomonas) conditions based off of new 'Pseudomonas' column and create new column 'CRP'
def CRP(s):
    if (s['Pseudomonas'] ==True) and ((s['Imipenem R'] == 'Resistant') or (s['Meropenem R'] == 'Resistant') or (s['Imipenem R'] == 'Intermediate') or (s['Meropenem R'] == 'Intermediate')):
        return '1'
    else:
        return '0'

transformed_data_df['CRP'] = transformed_data_df.apply(CRP, axis=1)
del transformed_data_df['Pseudomonas']


#save df as new csv
transformed_data_df.to_csv('#path to export new csv.csv')