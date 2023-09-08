import sqlite3

import pandas


def turn_into_sql():
    paths = [
        r'rozakhutor.csv',
    ]
    c = 0
    for path in paths:
        dataframe = pandas.read_csv(path, delimiter='\t')
        conn = sqlite3.connect(f'db_{c}.sqlite')
        dataframe.to_sql('database', conn)
        print(dataframe)
        c += 1


def extract_emails():
    db_name = r'db_0.sqlite'
    conn = sqlite3.connect(db_name)
    expr = "SELECT DISTINCT(lower(LOGIN)) FROM database WHERE LOGIN  LIKE '%@%'"

    cur = conn.cursor()
    cur.execute(expr)
    emails = [i[0] for i in cur.fetchall()]
    with open('rozakhutor.txt', 'w') as file:
        file.write('\n'.join(emails))
    breakpoint()


if __name__ == '__main__':
    # turn_into_sql()
    extract_emails()
