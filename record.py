"""
    分别完成csv/sqlte/postgres的记录
    
"""

def record_to_csv(file,data):
    import csv#
    
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

    return len(data)
#END record_to_csv

def record_to_sqlite(file,data):
    import sqlite3#

    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute( kp_sql_createtable('sqlite') ) 
    c.execute( kp_sql_inserts(data) )
    conn.commit()

    total_changes = conn.total_changes
    conn.close()
    return total_changes
#END record_to_sqlite


def record_to_postgres(dsn,data):
    import psycopg2#

    conn = psycopg2.connect("host=localhost dbname=test user=postgres password=pg123")
    cur = conn.cursor()
    cur.execute( kp_sql_createtable('postgres') )
    cur.execute( kp_sql_inserts(data) )
    conn.commit()

    total_changes = cur.rowcount
    cur.close()
    return total_changes
#END record_to_postgres

def kp_sql_createtable(type='sqlite'):
    sql = ''
    match type:
        case 'sqlite':
            sql='''CREATE TABLE IF NOT EXISTS `kp_nslookup` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`domain` VARCHAR(128) NOT NULL,
`ip` VARCHAR(16) NOT NULL,
`delay` FLOAT NOT NULL,
`checked` BOOLEAN NOT NULL DEFAULT 0,
`created` TIMESTAMP NOT NULL DEFAULT (DATETIME('now','localtime'))
);'''
        case 'postgres':
            sql = '''CREATE TABLE IF NOT EXISTS kp_nslookup (
id SERIAL PRIMARY KEY,
domain VARCHAR(128) NOT NULL,
ip VARCHAR(16) NOT NULL,
delay FLOAT NOT NULL,
checked SMALLINT NOT NULL DEFAULT 0,
created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP 
);'''
        case _:
            raise ValueError(f"maybe we no support mysql or {type}")
    return sql
#END kp_sql_createtable()

def kp_sql_inserts(data):
    sql = "INSERT INTO kp_nslookup (domain,ip,delay,checked) VALUES "
    vals = []
    for d in data:
        checked = d['check'] if d.__contains__('check') else 0
        domain = d['domain'] if d.__contains__('domain') else d['ip']
        vals.append(f"('{domain}','{d['ip']}',{d['delay']},{checked})")
    sql = f"{sql} {','.join(vals)} ;"
    return sql


def main():
    t_data = [{'ip': '16.163.84.236', 'delay': 102.23, 'check': 1}, {'ip': '18.163.65.176', 'delay': 102.43}]
    record_to_csv(file='hosts.csv',data=t_data)
    # record_to_sqlite('hosts.sqlite3', data=t_data)

    # dsn = "host=localhost dbname=test user=postgres password=***"
    # record_to_postgres(dsn,t_data)

if __name__ == '__main__':
    main()
