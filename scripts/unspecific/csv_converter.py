import pandas as pd
from ... import conf

for collection in conf.collection:
    csv_filename = 'csv/' + str(collection) + '.csv'

    read_file = pd.read_excel(conf.excel_filename, collection)
    read_file.to_csv(csv_filename,  
                    index = None, 
                    header=True)  
    df = pd.DataFrame(pd.read_csv(csv_filename))

    df

    print('Successfully converted {}:spreadsheet({}) into {}'.format(conf.excel_filename, collection, csv_filename))