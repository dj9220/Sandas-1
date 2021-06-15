import csv
import itertools
import operator
import sqlite3


def open_csv_task_1(fileName):
    with open(fileName) as File:
        data = csv.DictReader(File)
        _=next(data)
        names = sorted(data, key=operator.itemgetter('Darbuotojas'))
        salaries = itertools.groupby(names, operator.itemgetter('Darbuotojas'))
        print(salaries)
    return salaries
def write_to_csv_task_1(read_file, writing_file):
    taxes = open_csv_task_1(read_file)
    with open(writing_file, mode='w') as File:
        field_names = ['Darbuotojas', 'Suma', 'Mokesciai']
        writer = csv.DictWriter(File, fieldnames=field_names, delimiter = ';')
        writer.writeheader()
        for key, employee in taxes:
            total = sum(int(value['Alga']) for value in employee)
            fees = total * 0.4
            name = key
            writer.writerow({'Darbuotojas':name, 'Suma':total, 'Mokesciai':fees})

def open_csv_task_2(fileName):
    employees = []
    with open(fileName) as File, sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE data (Darbuotojas, Tipas, Alga)')
        db.executemany('INSERT INTO data VALUES (:Darbuotojas, :Tipas, :Alga)', csv.DictReader(File))
        cursor = db.execute('SELECT Darbuotojas, Tipas, SUM(Alga) AS Suma FROM data GROUP BY Darbuotojas, Tipas')
        for row in cursor:
            employee = {'Darbuotojas':row[0], 'Tipas':row[1], 'Alga':row[2]}
            employees.append(employee)
    return employees

def write_to_csv_task_2(fileName):
    employees = open_csv_task_2('duomenys.csv')
    with open(fileName, mode='w') as File:
        field_names = ['Darbuotojas', 'Tipas', 'Alga']
        writer = csv.DictWriter(File, delimiter = ';', fieldnames=field_names)
        writer.writeheader()
        for row in employees:
            writer.writerow(row)
if __name__ == '_main_':
    write_to_csv_task_1('duomenys.csv','rezultatai.csv')
    write_to_csv_task_2('rezultatai_2.csv')