from flask import Flask, render_template,url_for,redirect,request
import mysql.connector


app = Flask(__name__)



con = mysql.connector.connect(host="localhost",user="root",password="Bmthulasi1@",database="website")
web = con.cursor(dictionary=True)

@app.route("/",methods=['GET','POST'])
def home():
    msg = ""
    if request.method == 'POST':
      firstname = request.form['firstname']
      lastname = request.form['lastname']
      mobilenumber = request.form['mobilenumber']
      gmail = request.form['gmail']
      address = request.form['address']
      sql = "INSERT INTO user_image(firstname,lastname, mobilenumber,gmail,address)VALUES(%s,%s,%s,%s,%s)"
      web.execute(sql,[firstname,lastname,mobilenumber,gmail,address])
      res = web.fetchone
      con.commit()
      return redirect('account')
    return render_template("home.html",msg=msg)
@app.route("/account",methods=['GET','POST'])
def account():
    sql = "select * from user_image"
    web.execute(sql)
    res=web.fetchall()
    return render_template("account.html",datas=res)
@app.route("/delete/<id>",methods = ['GET','POST'])
def delete(id):
    web.execute("DELETE FROM user_image WHERE id=%s",[id])
    con.commit()
    return redirect(url_for('account'))
@app.route("/update/<id>",methods = ['GET','POST'])
def update(id):
    web=con.cursor(dictionary=True)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        mobilenumber = request.form['mobilenumber']
        gmail = request.form['gmail']
        address = request.form['address']
        sql = "UPDATE user_image SET firstname=%s , lastname=%s , mobilenumber=%s , gmail=%s , address=%s WHERE id=%s"
        web.execute(sql,[firstname,lastname,mobilenumber,gmail,address,id])
        return redirect(url_for('account'))

    sql = "SELECT * FROM user_image WHERE id = %s"
    web.execute(sql,[id])
    res = web.fetchone()
    return render_template("update.html",datas=res)

if __name__ in "__main__":
    app.run(debug=True)