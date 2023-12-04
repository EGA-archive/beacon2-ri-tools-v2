import pandas as pd
from scripts.datasheet.conf import conf


read_file = pd.read_excel (conf.excel_filename, conf.collection)
read_file.to_csv (conf.csv_filename,  
                  index = None, 
                  header=True)  
df = pd.DataFrame(pd.read_csv(conf.csv_filename))

df