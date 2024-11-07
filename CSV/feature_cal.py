import csv
import statistics

data = []

with open('csvFiles/sleep_cal.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(float(row[0]))
        
if data:
    print('平均：', sum(data) / len(data))
    print('中央値：', statistics.median(data))
    print('最小値：', min(data))
    print('最大値：', max(data))
    