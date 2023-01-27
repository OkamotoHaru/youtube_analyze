import csv
import os

def output(path, withoutExtension, data, encode):
    print('---csvClient.py output---')
    fileName = f'/{withoutExtension}.csv'
    filePath = os.getcwd() + path
    os.makedirs(filePath, exist_ok=True)
    with open(filePath + fileName, 'w', newline='', encoding=encode) as f:
        writer = csv.writer(
            f,
            lineterminator='\n',
        )
        writer.writerows(data)
    print(f'success: {filePath + fileName}')
    print('------')