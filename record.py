"""
    分别完成csv/sqlte/postgres的记录
    
"""

def record_to_csv(file,data):
    import csv
    
    labels = ['domain', 'ip', 'delay','check']
    try:
        with open(file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=labels)
            writer.writeheader()
            for elem in data:
                writer.writerow(elem)
                
    except IOError:
        print("I/O error")
        return False

    return True
#END record_to_csv





def main():
    t_data = [{'ip': '16.163.84.236', 'delay': 102.23, 'check': 1}, {'ip': '18.163.65.176', 'delay': 102.43}, {'ip': '18.167.219.46', 'delay': 105.52}, {'ip': '18.167.160.12', 'delay': 105.63}, {'ip': '18.166.243.220', 'delay': 105.71}, {'ip': '16.163.225.163', 'delay': 109.85}, {'ip': '18.163.151.37', 'delay': 114.68}, {'ip': '18.162.184.7', 'delay': 115.43}, {'ip': '13.225.78.24', 'delay': 203.28}, {'ip': '13.225.78.29', 'delay': 214.57}, {'ip': '13.225.78.126', 'delay': 219.87}, {'ip': '13.225.78.71', 'delay': 226.36}]
    record_to_csv(file='hosts.csv',data=t_data)

if __name__ == '__main__':
    main()
