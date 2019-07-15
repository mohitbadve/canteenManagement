from flask import Flask,request,render_template
import datetime
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form-report')
def formReport():
    searchedDates = []
    return render_template('sales_report.html',searchedDates = searchedDates)

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
    cur.close()
    con.close()
    #print(data)
    searchedDates= [fromDate,toDate]
    #print(searchedDates)
    return render_template('sales_report.html',data = data,searchedDates = searchedDates)

@app.route('/add-products',methods = ['POST'])
def addProducts():
    timeReq = float(request.form['timeReq'])
    price = float(request.form['price'])
    productName = request.form['productName']
    category = request.form['category']
    status = 'Available'
    productId = int(request.form['productIdActual'])
    login_id = 1
    date_of_record = datetime.datetime.now()
    con = pymysql.connect(
        host="localhost",
        user="mohit",
        passwd="Mohit@2K",
        database="canteen"
    )
    cur = con.cursor()
    try:
        print('Executing SQL')
        sql = "INSERT INTO products VALUES (%s, %s,%s,%s)"
        val = (productId,productName,category,status)
        cur.execute(sql, val)
        sql = "INSERT INTO price(product_id,price, date_of_record, login_id) VALUES (%s, %s,%s,%s)"
        val = (productId, price, date_of_record, login_id)
        cur.execute(sql, val)
        sql = "INSERT INTO time_required(product_id,time_required, date_of_record, login_id) VALUES (%s, %s,%s,%s)"
        val = (productId, timeReq, date_of_record, login_id)
        cur.execute(sql, val)
    except pymysql.InternalError as error:
        code, message = error.args
        print(">>>>>>>>>>>>>" +  str(code) +  str(message))
        return render_template('unsuccessful.html')
    con.commit()
    cur.close()
    con.close()
    return render_template('successful.html')


@app.route('/form-add-combos')
def formAddCombos():
    return render_template('add_combos.html')

@app.route('/form-add-products')
def formAddProducts():
    con = pymysql.connect(
        host="localhost",
        user="mohit",
        passwd="Mohit@2K",
        database="canteen"
    )
    cur = con.cursor()
    cur.execute("SELECT COUNT(idproducts) FROM products")
    data = cur.fetchone()
    productId = data[0]+1
    return render_template('add_products.html',productId = productId)

if __name__ == '__main__':
    app.run(debug=True)
