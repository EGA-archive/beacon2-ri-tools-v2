import pandas as pd
from scripts.datasheet.conf import conf

csv_filename = 'csv/' + conf.collection + '.csv'

read_file = pd.read_excel (conf.excel_filename, conf.collection)
read_file.to_csv (csv_filename,  
                  index = None, 
                  header=True)  
df = pd.DataFrame(pd.read_csv(csv_filename))

df

print('Successfully converted {}:spreadsheet({}) into {}'.format(conf.excel_filename, conf.collection, csv_filename))