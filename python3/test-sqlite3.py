import sqlite3

conn = sqlite3.connect('bxt.db3')
cur = conn.cursor()
cur.execute('create table bxt_trade_apply (id integer primary key, name varchar(50) unique, state varchar(1), year_rate varchar(6), to_end_days varchar(10), trade_num varchar(10), trade_amount varchar(10), url varchar(500), to_end_date varchar(500), start_buy_time varchar(500), end_buy_time varchar(500))')
conn.commit()
conn.close()
