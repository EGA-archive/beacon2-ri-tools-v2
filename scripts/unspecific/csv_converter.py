import pandas as pd
import csv

read_file = pd.read_excel ('/Users/oriol/Desktop/beacon-ri-tools-v2/datasheets/CINECA_synthetic_cohort_EUROPE_UK1.xlsx', 'genomicVariations')
read_file.to_csv ("CINECA.csv",  
                  index = None, 
                  header=True)  
df = pd.DataFrame(pd.read_csv("CINECA.csv"))

df