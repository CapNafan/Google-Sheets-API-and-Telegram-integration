import psycopg2
from dollar_rate import get_dollar_rate
from manage_sheets import get_data_from_sheets


def main():
    current_rate = get_dollar_rate()    # current USD rate from http://www.cbr.ru/scripts/XML_daily.asp
    print(current_rate)
    data = get_data_from_sheets()
    for item in data:
        print(item)


if __name__ == "__main__":
    main()
