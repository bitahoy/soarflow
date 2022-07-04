import csv
from datetime import date
from pickletools import long1
from typing import Any
from opensearchpy import OpenSearch, RequestsHttpConnection, helpers
import json
import math
es = OpenSearch([{'host': 'localhost', 'port': 9200}])
print(es)

def csv_reader(file_obj, delimiter=',', quoting=csv.QUOTE_NONNUMERIC):
    reader = csv.DictReader(file_obj)
    i = 1
    results = []
    csvFilePath = r'TFTP_mini.csv'
    jsonFilePath = r'./TFTP_mini4.json'
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        for row in reader:
            # es.index(index='phish_email', doc_type='doc', id=i,
            #                  body=json.dumps(row))
	    # _index with lowercase. no Uppercase
            index_row = {"index": {"_index": 'tftp_mini',
                                   # "_type": 'doc',
                                   '_id': i}}
            i = i + 1
            x = json.dumps(index_row)
            jsonf.write(x)
            jsonf.write("\n")
            y = json.dumps(row)
            python_data = json.loads(y)
            last_key = list(python_data)[-1]
            jsonf.write("{")
            for key in python_data:
                data = python_data[key]
                if isNumber(data) != True:
                    if key == ' Timestamp':
                        data = data[:10] + 'T' + data[11:]
                    jsonf.write(f'"{key}": "{data}"')
                else:
                    if data == 'inf':
                        data = 999999999
                    jsonf.write(f'"{key}": {data}')

                if key != last_key:
                    jsonf.write(",")
            jsonf.write("}")
            #jsonf.write(y)
            jsonf.write("\n")
    
def isNumber(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    with open("./TFTP_mini.csv") as f_obj:
        csv_reader(f_obj)
