from flask import Flask, render_template, request, redirect
import csv
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/newstudententry')
def newstudententry():
    return render_template('newstudententry.html')


@app.route('/searchstudent')
def searchstudent():
    return render_template('searchstudent.html')


@app.route('/process', methods=['POST'])
def process():
    id = request.form['id']
    std_name = request.form['std_name']
    gender = request.form['gender']
    dob = request.form['dob']
    city = request.form['city']
    state = request.form['state']
    email = request.form['email']
    qualification = request.form['qualification']
    stream = request.form['stream']

    newrow = [id, std_name, gender, dob, city,
              state, email, qualification, stream]

    with open('new.csv', 'a') as appendobj:
        append = csv.writer(appendobj)
        append.writerow(newrow)

    df = pd.read_csv('new.csv')
    df.dropna(axis=0, how='all', inplace=True)
    df.to_csv('new3.csv', index=False)

    return render_template('newstudententry.html', id=id, std_name=std_name, gender=gender, dob=dob, city=city, state=state, email=email, qualification=qualification, stream=stream)


@app.route('/process2', methods=['POST'])
def process2():
    df = pd.read_csv('new.csv')
    df.dropna(axis=0, how='all', inplace=True)
    df.to_csv('new3.csv', index=False)

    flag = True
    id = request.form['id']
    row_list = []
    csv_file = csv.reader(open('new3.csv', 'r'))
    for row in csv_file:
        if id == row[0]:
            row_list = row.copy()
            print(row_list)
        else:
            flag = False
    if flag == False:
        print('invalid')
    return render_template('searchstudent.html', id=id, row_list=row_list)


@app.route("/displaystudentlist")
def displaystudentlist():
    all_rows = []
    csv_file = csv.DictReader(open('new3.csv'))
    for rows in csv_file:
        all_rows.append(dict(rows))
    return render_template('displaystudentlist.html', all_rows=all_rows)


if __name__ == '__main__':
    app.run(debug=True)
