from flask import Flask,request,render_template
import datetime
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form-login',methods=['POST'])
def formLogin():
    type = request.form['type']
    print(type)
    return render_template('login.html',type = type)

@app.route('/login',methods=['POST'])
def login():
    type = request.form['type']
    login_id = request.form['login_id']
    password = request.form['password']
    con = pymysql.connect(
        host="localhost",
        user="mohit",
        passwd="Mohit@2K",
        database="canteen"
    )
    cur = con.cursor()
    sql = "SELECT COUNT(*) FROM login_data WHERE login_id = %s and password = %s and type = %s"
    val = (login_id,password,type)
    cur.execute(sql,val)
    data = cur.fetchall()
    cur.close()
    con.close()
    for item in data:
        print(item[0])
        if(item[0] == 1):
            if(type == 'Admin'):
                return render_template('admin.html')
            else:
                return render_template('staff.html')
        else:
            print(type)
            print(login_id)
            print(password)
            print(item[0])
            return render_template('unsuccessful.html')

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
    cur.execute("SELECT idorders,order_date,completion_date,status FROM orders WHERE order_date BETWEEN %s AND %s",(fromDate_obj,toDate_obj))
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
        cur.close()
        con.close()
        return render_template('unsuccessful.html')
    con.commit()
    cur.close()
    con.close()
    return render_template('successful.html')

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

@app.route('/menu')
def menu():
    con = pymysql.connect(
        host="localhost",
        user="mohit",
        passwd="Mohit@2K",
        database="canteen"
    )
    cur = con.cursor()
    sql = "select name,price,time_required,category from products inner join price on products.idproducts = price.product_id inner join time_required on products.idproducts = time_required.product_id where status = 'available' order by category"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    con.close()
    return render_template('menu.html',data = data,categoryPrinted = '')

@app.route('/form-remove-products')
def formRemoveProducts():
    con = pymysql.connect(
        host = 'localhost',
        user = 'mohit',
        passwd = 'Mohit@2K',
        database = 'canteen'
    )
    cur = con.cursor()
    sql = "SELECT idproducts,name FROM products WHERE status = 'available'"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    con.close()
    return render_template('remove_products.html',data = data)

@app.route('/remove-products',methods = ['POST'])
def removeProducts():
    productId = request.form['productId']
    con = pymysql.connect(
        host='localhost',
        user='mohit',
        passwd='Mohit@2K',
        database='canteen'
    )
    cur = con.cursor()
    try:
        sql = "UPDATE products SET status = 'Not available' WHERE idproducts = %s"
        val = (productId)
        cur.execute(sql,val)
        con.commit()
    except:
        cur.close()
        con.close()
        return render_template('unsuccessful.html')
    cur.close()
    con.close()
    return render_template('successful.html')

@app.route('/form-add-removed-products')
def formAddRemovedProducts():
    con = pymysql.connect(
        host = 'localhost',
        user = 'mohit',
        passwd = 'Mohit@2K',
        database = 'canteen'
    )
    cur = con.cursor()
    sql = "SELECT idproducts,name FROM products WHERE status = 'Not available'"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    con.close()
    return render_template('add_removed_products.html',data = data)

@app.route('/add-removed-products',methods = ['POST'])
def addRemovedProducts():
    productId = request.form['productId']
    con = pymysql.connect(
        host='localhost',
        user='mohit',
        passwd='Mohit@2K',
        database='canteen'
    )
    cur = con.cursor()
    try:
        sql = "UPDATE products SET status = 'Available' WHERE idproducts = %s"
        val = (productId)
        cur.execute(sql,val)
        con.commit()
    except:
        cur.close()
        con.close()
        return render_template('unsuccessful.html')
    cur.close()
    con.close()
    return render_template('successful.html')

@app.route('/form-place-order')
def formPlaceOrder():
    con = pymysql.connect(
        host='localhost',
        user='mohit',
        passwd='Mohit@2K',
        database='canteen'
    )
    cur = con.cursor()
    sql = "SELECT name FROM products WHERE status = 'Available'"
    cur.execute(sql)
    productNames = cur.fetchall()
    sql = "SELECT COUNT(*) FROM products WHERE status = 'Available'"
    cur.execute(sql)
    countNames = cur.fetchall()
    return render_template('place_order.html',productNames = productNames,countNames = countNames)

@app.route('/form-update-order-status')
def formUpdateOrder():
    return render_template('update_order_status.html',orders = '',table_id = -1,idorders = -1)

@app.route('/get-orders',methods=['POST'])
def getOrders():
    table_id = request.form['table_id']
    con = pymysql.connect(
        host='localhost',
        user='mohit',
        passwd='Mohit@2K',
        database='canteen'
    )
    cur = con.cursor()
    sql = "SELECT idorders,order_date,status FROM orders WHERE table_id = %s"
    val = (table_id)
    cur.execute(sql,val)
    orders = cur.fetchall()
    cur.close()
    con.close()
    return render_template('update_order_status.html',orders = orders,table_id = table_id,idorders = -1)

@app.route('/update-order-status/<idorders>',methods=['POST'])
def updateOrder(idorders):
    print(idorders)
    return render_template('update_order_status.html',orders = '',idorders = idorders,table_id = '')

@app.route('/order-status-final',methods=['POST'])
def orderStatus():
    idorders = int(request.form['idorders'])
    status = request.form['status']
    print(idorders)
    print(status)
    con = pymysql.connect(
        host='localhost',
        user='mohit',
        passwd='Mohit@2K',
        database='canteen'
    )
    cur = con.cursor()
    if(status == 'Completed'):
        completion_date = datetime.datetime.now()
        sql = "UPDATE orders SET status = %s,completion_date = %s WHERE idorders = %s"
        val = (status,completion_date,idorders)
    else:
        sql = "UPDATE orders SET status = %s,completion_date = NULL WHERE idorders = %s"
        val = (status,idorders)
    cur.execute(sql,val)
    con.commit()
    cur.close()
    con.close()
    return render_template('successful.html')

@app.route('/form-add-combos')
def formAddCombos():
    con = pymysql.connect(
        host='localhost',
        user='mohit',
        passwd='Mohit@2K',
        database='canteen'
    )
    cur = con.cursor()
    sql = "SELECT name FROM products WHERE status = 'available'"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    con.close()
    return render_template('add_combos.html',data = data)

@app.route('/add-combos',methods = ['POST'])
def addCombos():
    productNames = request.form['dropdown']
    print(productNames)
    return render_template('successful.html')


if __name__ == '__main__':
    app.run(debug=True)
