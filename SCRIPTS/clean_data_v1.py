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

        # GET SELLER TAX_NO
        json_string = row.seller_tax_no.replace("\'", "\"")
        data = json.loads(json_string)
        obj_seller_tax_no = data[0]
        obj_buyer_tax_no = data[1]
        print(obj_seller_tax_no)
        print(obj_buyer_tax_no)
        df.loc[row.Index, 'seller_tax_no'] = obj_seller_tax_no

        # GET BUYER TAX_NO
        # json_string = row.buyer_tax_no.replace("\'", "\"")
        # data = json.loads(json_string)
        # obj = data[0]
        # print(obj)
        df.loc[row.Index, 'buyer_tax_no'] = obj_buyer_tax_no

        # CLEAN DATA
        # df.loc[row.Index, 'seller_name'] = row.seller_name.replace("Tên người bán:", "")
        # df.loc[row.Index, 'buyer_name'] = row.buyer_name.replace("Tên người mua:", "")
        # df.loc[row.Index, 'buyer_fullname'] = row.buyer_fullname.replace("Họ tên người mua:", "")

        # GET ITEMS
        json_string = row.lines.replace("\'", "\"")
        # print(json_string)

        data = json.loads(json_string)
        obj = data[0]
        print(obj)

        df.loc[row.Index, 'product_name'] = obj['product_name']
        df.loc[row.Index, 'unit'] = obj['unit']
        df.loc[row.Index, 'qty'] = obj['qty']
        df.loc[row.Index, 'price'] = obj['price']
        df.loc[row.Index, 'total_amount'] = obj['amount_untaxed']

    except Exception as e:
        # Print the exception message
        print("An exception occurred:", str(e))

# print(df)

df.to_csv('invoices-output-final.csv', encoding='utf-8', index=False)
