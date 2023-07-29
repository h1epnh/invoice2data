import pandas as pd
import re
import datetime
from datetime import datetime as dt
import json


def convert_str_to_list(str):
    # Converting string to list
    return str.strip('][').split(', ')


def get_tax(tax_list_tr):
    tax_list = convert_str_to_list(tax_list_tr)
    # filter to get right TaxNo
    tax_no = [i for i in tax_list if i.find("-") > 0]
    return tax_no


df = pd.read_csv('/Users/admin/@Programming/VICTORY EXPRESS/invoice2data/invoices-output.csv', dtype=str)

# print(df.info())

DEBUG = '1'

for row in df.itertuples(index=True, name='Pandas'):
    # print(row.invoice_number)

    try:
        # json_string = row.lines.replace("\'", "\"").strip('][')

        json_string = row.lines.replace("\'", "\"")
        # print(json_string)

        data = json.loads(json_string)
        obj = data[0]
        print(obj)

        df.loc[row.Index, 'service'] = obj['service']
        df.loc[row.Index, 'unit'] = obj['unit']
        df.loc[row.Index, 'qty'] = obj['qty']
        df.loc[row.Index, 'price'] = obj['price']
        df.loc[row.Index, 'discount'] = obj['discount']
        df.loc[row.Index, 'tax'] = obj['tax']
        df.loc[row.Index, 'total_amount'] = obj['amount_untaxed']

    except Exception as e:
        # Print the exception message
        print("An exception occurred:", str(e))

# print(df)

df.to_csv('invoices-output-final.csv', encoding='utf-8', index=False)
