import csv

l = [[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]]
print(l)
# [[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]]

with open('C:/Users/inaga/OneDrive/ドキュメント/Python_files/csv/huga.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(l)