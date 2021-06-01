from abc import ABCMeta
from typing import Tuple
from flask import Flask, render_template, redirect, url_for, abort, request, flash, session
from flask.globals import session
from flask_mysqldb import MySQL
from datetime import date,timedelta

app = Flask(__name__)
app.secret_key = 'hello'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tanAvan2596'
app.config['MYSQL_DB'] = 'lib'

mysql = MySQL(app) #SETTING MYSQL CONNECTION

class formdata:
    def __init__(self, bookids, uid, eid, amt, c) :
        self.bookids = bookids
        self.uid = uid
        self.eid = eid
        self.amt = amt
        self.c = c

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    if 'username' in session:
        email=session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE EMAIL = %s", (email, ))
        userinfo = cur.fetchone()
        print(userinfo)
        cur.close()
        return render_template('account.html', userinfo=userinfo)
    return redirect('/login')

@app.route('/change/')
def change():
    if 'username' in session:
        what=request.args.get('what', None)
        email=session['username']
        cur=mysql.connection.cursor()
        if what == 'ADDRESS':
            cur.execute("SELECT ADDR FROM USERS WHERE EMAIL = %s", (email, ))
        if what == 'PASSWORD':
            cur.execute("SELECT PW FROM USERS WHERE EMAIL = %s", (email, ))
        if what == 'PHONE NUMBER':
            cur.execute("SELECT PHONENO FROM USERS WHERE EMAIL = %s", (email, ))
        res=cur.fetchone()
        cur.close()
        return render_template('change.html', res=res, what=what, email=email)
    return redirect('/login')

@app.route('/changeresult/', methods=['GET', 'POST'])
def changeresult():
    if 'username' in session:
        flag=request.args.get('flag', None)
        email=session['username']
        if request.method == 'POST':
            details = request.form
            cur=mysql.connection.cursor()
            if flag == 'ADDRESS':
                cur.execute("UPDATE USERS SET ADDR = %s WHERE EMAIL = %s", (details['address'], email,))
                flash('ADDRESS UPDATED')
                mysql.connection.commit()
            if flag == 'PHONE NUMBER':
                cur.execute("UPDATE USERS SET PHONENO = %s WHERE EMAIL = %s", (details['phoneno'], email,))
                flash('PHONE NUMBER UPDATED')
                mysql.connection.commit()
            if flag == 'PASSWORD':
                cur.execute("SELECT PW FROM USERS WHERE EMAIL = %s", (email, ))
                curpw=cur.fetchone()
                if details['oldpw'] != curpw[0]:
                    flash('OLD PASSWORD INCORRECT')
                    return render_template('change.html', res=curpw, what=flag, email=email)
                if details['newpw'] != details['confnewpw']:
                    flash('NEW PASSWORD AND CONFIRM PASSWORD DO NOT MATCH')
                    return render_template('change.html', res=curpw, what=flag, email=email)
                cur.execute("UPDATE USERS SET PW = %s WHERE EMAIL = %s", (details['confnewpw'], email, ))
                flash('PASSWORD UPDATED')
                mysql.connection.commit()
            cur.execute("SELECT * FROM USERS WHERE EMAIL = %s", (email, ))
            tup_item=cur.fetchone()
            cur.close()
            return render_template('options_page.html', tup_items=tup_item)
    return redirect('/login')

@app.route('/delaccount/')
def delaccount():
    if 'username' in session:
        email=request.args.get('email', None) #HAS ANY EMAIL ID OR THE WORD 'YES'
        if email == 'YES':
            email=session['username'] #'YES' IS OVERWRITTEN WITH LOGGED IN EMAIL
            cur=mysql.connection.cursor()
            cur.execute("SELECT UID FROM USERS WHERE EMAIL = %s", (email, ))
            res=cur.fetchone()
            myuid=res[0]
            cur.execute("SELECT COUNT(OID) FROM ORDERS WHERE UID = %s AND OSTATUS='D'", (myuid,))
            res=cur.fetchone()
            if res[0] != 0:
                flash('ACCOUNT CAN BE DELETED ONLY AFTER RETURNING ALL THE BOOKS')
                return redirect(url_for('options_page', email=email))
            cur.execute("SELECT OID, EID FROM ORDERS WHERE UID = %s AND OSTATUS = 'O'", (myuid,))
            myord=cur.fetchall() #tuple of tuples
            mylist =[]
            mylist3=[]
            for tup in myord: #selecting each tuple
                mylist.append(tup[0]) #oid
                mylist3.append(tup[1]) #eid
            print('oids: ',mylist)
            print('eids: ',mylist3)

            if len(mylist)!=0 : #if there are a few orders to be cancelled
                format_strings = ','.join(['%s'] * len(mylist))
                cur.execute("SELECT BID FROM ODETAILS WHERE OID IN (%s)" % format_strings, tuple(mylist))
                mybids=cur.fetchall()

                mylist2=[]
                for tup in mybids: #selecting each tuple
                    mylist2.append(tup[0]) #bid
                print('bids: ',mylist2)
                format_strings = ','.join(['%s'] * len(mylist2))
                cur.execute("UPDATE BOOK SET BSTATUS='A', BORROWEDBY=NULL WHERE BID IN (%s)" %format_strings, tuple(mylist2))
                mysql.connection.commit()
                format_strings = ','.join(['%s'] * len(mylist3))
                cur.execute("UPDATE DELPPL SET ORDERCOUNT = ORDERCOUNT-1 WHERE EID IN (%s)" %format_strings, tuple(mylist3))
                mysql.connection.commit()

            cur.execute("DELETE FROM ODETAILS WHERE OID IN (SELECT OID FROM ORDERS WHERE UID = %s)",(myuid, ))
            mysql.connection.commit()
            cur.execute("DELETE FROM ORDERS WHERE UID = %s", (myuid, ))
            mysql.connection.commit()
            cur.execute("DELETE FROM USERS WHERE UID = %s", (myuid, )) #can be done with email also
            mysql.connection.commit()
            return redirect('/logout')
        flash('ARE YOU SURE TO DELETE THE ACCOUNT ?')
        email=session['username'] #ANY INVALID EMAIL IS OVERWRITTEN
        return render_template('del.html', email=email)
    return redirect('/login')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        flash('LOGGED OUT')
        print(session)
        return redirect('/')
    return redirect('/login')

@app.route('/options/')
def options_page():
    if 'username' in session: #logged in
        email = session['username'] #email is always logged in email
        print(session)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM USERS WHERE EMAIL = %s", (email,))
        result = cur.fetchone()
        return render_template('options_page.html', tup_items = result)
    return redirect('/login') #not logged in

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        mail = details['mail']
        phno = details['phoneno']
        Addr = details['addr']
        pw = details['pw']
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM USERS WHERE EMAIL = %s", (mail,))
        result = cur1.fetchall()
        if(len(result)): #if email already exists , go to login
            cur1.close()
            flash("EMAIL ALREADY EXISTS , PLEASE LOGIN")
            return redirect('/login')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO USERS (FNAME, LNAME, EMAIL, PHONENO, ADDR, PW) VALUES (%s, %s, %s, %s, %s, %s )", (firstName, lastName, mail, phno, Addr, pw))
            mysql.connection.commit()
            cur.close()
            session['username']=mail
            return redirect(url_for('options_page', email = mail))
    return render_template('register_dbms.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        details = request.form
        mail = details['mail']
        pw = details['pw']
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT * FROM USERS WHERE EMAIL = %s", (mail, ))
        result = cur1.fetchall()
        pw_conf = ''
        if len(result) == 0:
            flash('EMAIL DOES NOT EXIST , PLEASE REGISTER')
            return redirect('/register') #email does not exist
        for x in result: #email exists
            pw_conf = x[6]
            if pw_conf != pw:
                flash("PASSWORD INCORRECT")
                cur1.close()
                return redirect('/login')
        cur1.close()
        session['username']=mail
        return redirect(url_for('options_page', email = mail)) #on successful login
    return render_template('login_dbms.html')

form_list = []
@app.route('/borrow/<email>', methods=['GET', 'POST'])
def borrow(email):
    if 'username' in session:
        email = session['username']
        if request.method == 'POST':
            #FETCHING THE UID OF PERSON LOGGED IN
            cur1 = mysql.connection.cursor()
            cur1.execute("SELECT * FROM USERS WHERE EMAIL = %s", (email, ))
            u = cur1.fetchone() #USERDETAILS
            cur1.close()
            uid = u[0] #getting the uid of the person logged in

            mylist = request.form.getlist('mycheckbox')
            if len(mylist) == 0 :
                flash('PLEASE SELECT A BOOK')
                return redirect(url_for('borrow', email = email))
            print(mylist)
            req = len(mylist) #COUNTS THE NUMBER OF BOOKS CHECKED
            cur1  = mysql.connection.cursor()
            cur1.execute("SELECT COUNT(*) FROM BOOK WHERE BSTATUS = 'B' AND BORROWEDBY = (SELECT UID FROM USERS WHERE EMAIL = %s)", (email, ))
            res = cur1.fetchall()
            cur1.close()

            # MAX 4 BOOKS PER PERSON
            if req + res[0][0] > 4:
                flash("Maximum 4 books allowed to be borrowed by per person, please choose lesser number of books")
                return redirect(url_for('borrow', email = email))

            #GETTING EID
            cur =  mysql.connection.cursor()
            cur.execute("SELECT * FROM DELPPL WHERE ORDERCOUNT = (SELECT MIN(ORDERCOUNT) FROM DELPPL)")
            emp = cur.fetchone() #EMP DETAILS
            ans = emp[0] #HAS THAT EID
            #CALCULATING SUM
            cur.execute("SELECT SUM(PRICE) FROM BOOK WHERE BID IN %(ret)s", {'ret':tuple(mylist)})
            answer = cur.fetchone()
            amt  = answer[0]

            cur.execute("SELECT * FROM BOOK WHERE BID IN %(ret)s", {'ret':tuple(mylist)})
            mybooks = cur.fetchall()

            c=emp[4]+2 #no of days btwn order date and delivery date
            odate = date.today()
            ddate = odate+timedelta(c)
            if c>4:
                flash("Expected delivery date is later than usual. All our delivery executives are busy at the moment.")
            cur.close()
            mydata = formdata(mylist, u[0], emp[0], amt, c)
            form_list.clear()
            form_list.append(mydata)
            print('object', mydata.bookids)
            print('form_list', form_list[0].bookids)
            return render_template('confirm.html', books = mybooks, u = u, emp = emp, tot = amt, odate = odate, ddate = ddate)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BOOK WHERE BSTATUS = 'A'")
        result = cur.fetchall()
        cur.execute("SELECT * FROM BOOK WHERE BSTATUS = 'B'")
        res1=cur.fetchall()
        return render_template('borrow.html', books = result, mail = email, booksbor=res1)
    return redirect('/login') #not logged in

@app.route('/confirm/<email>', methods = ['GET', 'POST'])
def confirm(email):
    if 'username' in session:
        email=session['username']
        if request.method == 'POST':
            myformobj = form_list[0]
            for x in myformobj.bookids:
               print(x)
            #UPDATING THE BOOK TABLE
            cur = mysql.connection.cursor()
            for x in myformobj.bookids:
                cur.execute("UPDATE BOOK SET BSTATUS = 'B', BORROWEDBY = (SELECT UID FROM USERS WHERE EMAIL = %s) WHERE BID  = %s", (email, x, ))
                mysql.connection.commit()

            #UPDATING THE DELIVERY PEOPLE TABLE
            cur.execute("UPDATE DELPPL SET ORDERCOUNT = ORDERCOUNT + 1 WHERE EID = %s", (myformobj.eid, ))
            mysql.connection.commit()

            #INSERT INTO ORDERS
            cur.execute("INSERT INTO ORDERS (UID, EID, AMOUNT,FINE, TOTAL, OSTATUS) VALUES (%s, %s, %s, %s, %s, %s)", (myformobj.uid, myformobj.eid, myformobj.amt, 0, myformobj.amt,  'O', ))
            mysql.connection.commit()

            cur.execute("SELECT MAX(OID) FROM ORDERS")
            oids=cur.fetchone() #just to double check whether correct oid is inserted for odetails
            print('oids: ', oids)
            #INSERT INTO ODETAILS
            for x in myformobj.bookids:
                cur.execute("SELECT PRICE FROM BOOK WHERE BID = %s", (x, ))
                req_price = cur.fetchone()
                cur.execute("INSERT INTO ODETAILS (OID, BID, PRICE) VALUES (%s, %s, %s)", (oids[0], x, req_price[0], ))
                mysql.connection.commit()

            flash("ORDER TAKEN")
            return redirect(url_for('options_page', email = email))
    return redirect('/login') #not logged in

@app.route('/return_book/<email>')
def return_book(email):
    if 'username' in session:
        email=session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM ORDERS WHERE (UID = (SELECT UID FROM USERS WHERE EMAIL = %s) AND OSTATUS = 'D')", (email, ))
        items = cur.fetchall()
        print(items)
        if len(items) == 0 :
            flash("NO ORDERS DELIVERED YET")
        cur.execute("SELECT ODETAILS.OID, BOOK.BNAME, BOOK.AUTHOR, BOOK.PRICE FROM ORDERS INNER JOIN ODETAILS ON ORDERS.OID=ODETAILS.OID INNER JOIN BOOK ON ODETAILS.BID=BOOK.BID WHERE ORDERS.UID=(SELECT UID FROM USERS WHERE EMAIL = %s)", (email, ))
        odeets = cur.fetchall()
        cur.close()
        return render_template('return_books.html', email =email, orders = items, odeets=odeets)
    return redirect('/login')

@app.route('/returnConfirm')
def returnConfirm():
    if 'username' in session:
        email=session['username']
        oid=request.args.get('oid',None)
        dt = date.today()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE ORDERS SET OSTATUS = 'R', RDATE = %s WHERE OID = %s", (dt, oid, ))
        mysql.connection.commit()
        cur.execute("UPDATE BOOK SET BSTATUS = 'A', BORROWEDBY = NULL WHERE BID IN (SELECT BID FROM ODETAILS WHERE OID = %s)", (oid,))
        mysql.connection.commit()
        cur.execute("SELECT * FROM USERS WHERE EMAIL = %s", (email, ))
        userinfo = cur.fetchone()
        cur.close()
        flash("RETURN INITIATED, PLEASE KEEP THE TOTAL AMOUNT IN CASH")
        return render_template('options_page.html', tup_items=userinfo)
    return redirect('/login') #not logged in

@app.route('/view_orders/<email>')
def view_orders(email):
    if 'username' in session:
        email=session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT ORDERS.*, DELPPL.FNAME, DELPPL.LNAME, DELPPL.PHONENO FROM ORDERS INNER JOIN DELPPL ON ORDERS.EID = DELPPL.EID WHERE ORDERS.UID=(SELECT UID FROM USERS WHERE EMAIL = %s) ORDER BY OID DESC", (email, ))
        orders = cur.fetchall()

        cur.execute("SELECT ODETAILS.OID, BOOK.BNAME, BOOK.AUTHOR, BOOK.PRICE FROM ORDERS INNER JOIN ODETAILS ON ORDERS.OID = ODETAILS.OID INNER JOIN BOOK ON ODETAILS.BID = BOOK.BID WHERE ORDERS.UID = (SELECT UID FROM USERS WHERE EMAIL = %s)", (email, ))
        odetails = cur.fetchall()
        cur.close()
        if len(orders)==0:
            flash('NO ORDERS YET')
        return render_template('view_orders.html', orders = orders, odetails = odetails, email = email)
    return redirect('/login') #if not logged in

if __name__ ==  "__main__":
    app.run(debug=True)
