import psycopg2
import time
from datetime import datetime
from config import host, user, password
from manage_sheets import get_data_from_sheets
from dollar_rate import get_dollar_rate

insert_query = '''INSERT INTO orders(id, order_num, cost_usd, cost_rub, delivery_date) 
                              Values(%s,%s,%s,%s,%s);'''
delete_query = 'DELETE FROM orders WHERE id = %s'
update_query = '''UPDATE orders SET id = %s, order_num = %s, 
                                    cost_usd = %s, cost_rub = %s, delivery_date = %s 
                                WHERE id = %s'''

while True:
    usd_rate = get_dollar_rate()  # current USD rate from http://www.cbr.ru/scripts/XML_daily.asp

    table = get_data_from_sheets()
    for row in table:
        row.insert(3, row[2] * usd_rate)  # inserted cost in rubles
        row[4] = datetime.strptime(row[4], '%d.%m.%Y').date()
    print(table)

    table_ids = set([i[0] for i in table])  # created set for faster membership tests
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            # checking existence of table "orders"
            cursor.execute(f"select exists(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('orders',))
            if not cursor.fetchone()[0]:
                # creating one if it doesn't exist
                cursor.execute("""CREATE TABLE orders(
                                id int,
                                order_num int,
                                cost_usd int,
                                cost_rub real,
                                delivery_date date)  
                                """)
                print('created table')
            cursor.execute('SET datestyle TO "ISO, DMY";')  # changing table datestyle to dd/mm/yyyy format

            cursor.execute("SELECT * FROM orders LIMIT 1;")
            if not cursor.fetchone():   # If the table is empty it is filled with data from table
                for row in table:
                    cursor.execute(insert_query, (*row, ))

            else:
                cursor.execute('SELECT id FROM orders;')
                database_ids = set([tp[0] for tp in cursor.fetchall()])

                # searching ids to delete from DB
                for _id in database_ids:
                    if _id not in table_ids:
                        cursor.execute(delete_query, (_id, ))
                        print('deleted', _id)

                # searching ids to add to DB
                table_dict = {row[0]: row[1:] for row in table}
                print(table_dict)
                for _id in table_ids:
                    if _id not in database_ids:
                        cursor.execute(insert_query, (_id, *table_dict[_id],))
                        print('inserted', _id)

                # creating and comparing sets of data from DB and from Google sheets
                cursor.execute('SELECT id, order_num, cost_usd, delivery_date FROM orders;')
                from_db = set(cursor.fetchall())
                from_sheets = {(row[0], row[1], row[2], row[4]) for row in table}

                difference = from_sheets - from_db

                # updating DB with changed rows
                for element in difference:
                    cursor.execute(update_query, (*element[:3], element[2]*usd_rate, element[3], element[0]))

        time.sleep(3)   # sleep for 3 sec to avoid exceeding 'Read requests per minute per user'

    # except Exception as exc:
    #     print('[ERROR]', exc)

    finally:
        if connection:
            connection.close()