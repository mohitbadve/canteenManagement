from flask import Flask,request,render_template
import datetime
import pymysql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form-report')
def formReport():
    return render_template('sales_report.html')

@app.route('/report',methods = ['POST'])
def report():
    fromDate = request.form['from']
    toDate = request.form['to']
    fromDate_obj = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
    toDate_obj = datetime.datetime.strptime(toDate, '%Y-%m-%d')
    con = pymysql.connect(
        host="localhost",
        user="mohit",
        passwd="Mohit@2K",
        database="canteen"
    )
    cur = con.cursor()
    print(fromDate_obj)
    print(toDate_obj)
    cur.execute("SELECT * FROM orders WHERE order_date BETWEEN %s AND %s",(fromDate_obj,toDate_obj))
    data = cur.fetchall()
    print(data)
    return render_template('sales_report.html',data = data)

if __name__ == '__main__':
    app.run(debug=True)
