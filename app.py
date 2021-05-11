from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from sendemail import sendgridmail
import smtplib
xyza = ''


  
app = Flask(__name__)
  
app.secret_key = 'a'

  
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'Yuz01g2mSe'
app.config['MYSQL_PASSWORD'] = 'aG6SA4kWBb'
app.config['MYSQL_DB'] = 'Yuz01g2mSe'
mysql = MySQL(app)

@app.route('/')
def homepagea():
    return render_template('homepage.html')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
@app.route('/customerforgot',methods =['GET', 'POST'])
def customerforgot():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username,email FROM customerregistrationa WHERE username = % s AND email = % s', (username, email ))
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
        
            
            username = account[0]
            email=  account[1]
            
        
        

            cursor = mysql.connection.cursor()
            print("sucess")
            cursor.execute('UPDATE customerregistrationa SET password=% s WHERE username  =% s  AND email=%s ',(password,username,email))
            mysql.connection.commit()
            cursor.execute('UPDATE customerlogin SET password=% s WHERE username  =% s  ',(password,username))
        
        
            mysql.connection.commit()
            
        
            msg = 'You have successfully Reset the Password !'
            TEXT = "Hello "+username + ",\n\n"+ """ Reset the password at digital payment book, Sucessfuly """ 
            TEXTT = "Hello "+username + ",\n\n"+ """as Reset the password at digital payment book """ 
            message  = 'Subject: {}\n\n{}'.format("Digital Payment Book", TEXT)
            #sendmail(TEXT,email)
            sendgridmail(email,TEXTT,TEXT)
    
            return render_template('customerforgot.html', msg = msg)
        else:
            msg = 'Incorrect username / email !'
    
    return render_template('customerforgot.html', msg = msg)
    
    
@app.route('/adminlogin',methods =['GET', 'POST'])
def adminlogin():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM adminlogin WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            cursor = mysql.connection.cursor()
            
            
            cursor.execute('SELECT sum(yougive) FROM admincustomer' )
            al = cursor.fetchone()[0]
            cursor.execute('SELECT sum(pending) FROM admincustomer' )
            bl = cursor.fetchone()[0]
            cursor.execute('SELECT * FROM admincustomer' )
            account = cursor.fetchall()
            ss=len(account)
            print("Total rows are:", len(account))
            print("Printing for each row")
            print("accountdislay",account)
            print(al,bl)
            print(al,bl)
            ac=int(0)
            if al is None  and bl is None:
                al=int(0)
                bl=int(0)
            
            elif al is None:
                al=int(0)
            elif bl is None:
                bl=int(0)
            if al>bl:
                ak=al-bl
                return render_template('adminadashboard.html',account=account,len=len(account), msg = msg,ak=ak)
            elif bl>al:
                am=bl-al
                return render_template('adminadashboard.html',account=account,len=len(account), msg = msg,am=am)
            else :
                cursor = mysql.connection.cursor()
                return render_template('adminadashboard.html',account=account,len=len(account), msg = msg,ac=ac)


            
        else:
            msg = 'Incorrect username / password !'
    
    return render_template('adminlogin.html', msg = msg)

@app.route('/customerlogin',methods =['GET', 'POST'])
def customerlogin():
    global userid
    ac=int(0)
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        
        
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM customerlogin WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            cursor = mysql.connection.cursor()
            
            paymethod="You Got"
            paymethodl="You Give"
            cursor.execute('SELECT sum(amount) FROM customerdetails WHERE username = % s AND paymethod = % s', (username, paymethod ),)
            al = cursor.fetchone()[0]
            
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT sum(amount) FROM customerdetails WHERE username = % s AND paymethod = % s', (username, paymethodl ),)
            bl = cursor.fetchone()[0]
            
            print(al,bl)
            print(al,bl)
            cursor.execute('SELECT * FROM customerdetails WHERE username  =% s ',( username,))
            account = cursor.fetchall()
            ss=len(account)
            print("Total rows are:", len(account))
            print("Printing for each row")
            print("accountdislay",account)
            print(al,bl)
            print(al,bl)
            
       
            if al is None  and bl is None:
                al=int(0)
                bl=int(0)
            
            elif al is None:
                al=int(0)
            elif bl is None:
                bl=int(0)
       
            if al>bl:
                ak=al-bl
                cursor = mysql.connection.cursor()
                bn=int(0)
                all=cursor.execute('UPDATE admincustomer SET yougive=% s,pending=% s WHERE username  =% s ',(ak,bn, username))
                mysql.connection.commit()
                print(all)
                
        

            
                return render_template('customerdashboard.html',account=account,len=len(account), msg = msg,ak=ak)
            elif bl>al:
                am=bl-al
                cursor = mysql.connection.cursor()
                bn=0
                all=cursor.execute('UPDATE admincustomer SET  yougive=% s,pending=% s WHERE  username=% s',(bn,am, username))
                mysql.connection.commit()
                print(all)
                

                return render_template('customerdashboard.html',account=account,len=len(account), msg = msg,am=am)
            else :
                cursor = mysql.connection.cursor()
                bn=int(0)
                all=cursor.execute('UPDATE admincustomer SET yougive=% s,pending=% s WHERE username  =% s ',( ac,bn,username))
                mysql.connection.commit()
                print(all)
                
                return render_template('customerdashboard.html',account=account,len=len(account), msg = msg,ac=ac)


            print(al)
            print(bl)
            
            
            
        else:
            msg = 'Incorrect username / password !'
    
    return render_template('customerlogin.html', msg = msg)

  

@app.route('/adminadashboard')
def adminadashboard():
            cursor = mysql.connection.cursor()
            msg = ''
            
            
            cursor.execute('SELECT sum(yougive) FROM admincustomer' )
            al = cursor.fetchone()[0]
            cursor.execute('SELECT sum(pending) FROM admincustomer' )
            bl = cursor.fetchone()[0]
            cursor.execute('SELECT * FROM admincustomer' )
            account = cursor.fetchall()
            ss=len(account)
            print("Total rows are:", len(account))
            print("Printing for each row")
            print("accountdislay",account)
            print(al,bl)
            print(al,bl)
            ac=int(0)
            if al is None  and bl is None:
                al=int(0)
                bl=int(0)
            
            elif al is None:
                al=int(0)
            elif bl is None:
                bl=int(0)
            if al>bl:
                ak=al-bl
                return render_template('adminadashboard.html',account=account,len=len(account), msg = msg,ak=ak)
            elif bl>al:
                am=bl-al
                return render_template('adminadashboard.html',account=account,len=len(account), msg = msg,am=am)
            else :
                cursor = mysql.connection.cursor()
                return render_template('adminadashboard.html',account=account,len=len(account), msg = msg,ac=ac)

@app.route('/customerdashboard',methods =['GET', 'POST'])
def customerdashboard():
            global userid
            ac=int(0)
            username=session['username']
            print(username)
            msg=''
        
            cursor = mysql.connection.cursor()
            
            paymethod="You Got"
            paymethodl="You Give"
            cursor.execute('SELECT sum(amount) FROM customerdetails WHERE username = % s AND paymethod = % s', (username, paymethod ),)
            al = cursor.fetchone()[0]
            
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT sum(amount) FROM customerdetails WHERE username = % s AND paymethod = % s', (username, paymethodl ),)
            bl = cursor.fetchone()[0]
            
            print(al,bl)
            print(al,bl)
            cursor.execute('SELECT * FROM customerdetails WHERE username  =% s ',( username,))
            account = cursor.fetchall()
            ss=len(account)
            print("Total rows are:", len(account))
            print("Printing for each row")
            print("accountdislay",account)
            print(al,bl)
            print(al,bl)
            
       
            if al is None  and bl is None:
                al=int(0)
                bl=int(0)
            
            elif al is None:
                al=int(0)
            elif bl is None:
                bl=int(0)
       
            if al>bl:
                ak=al-bl
                cursor = mysql.connection.cursor()
                bn=int(0)
                all=cursor.execute('UPDATE admincustomer SET yougive=% s,pending=% s WHERE username  =% s ',(ak,bn, username))
                mysql.connection.commit()
                print(all)
                
        

            
                return render_template('customerdashboard.html',account=account,len=len(account), msg = msg,ak=ak)
            elif bl>al:
                am=bl-al
                cursor = mysql.connection.cursor()
                bn=0
                all=cursor.execute('UPDATE admincustomer SET  yougive=% s,pending=% s WHERE  username=% s',(bn,am, username))
                mysql.connection.commit()
                print(all)
                

                return render_template('customerdashboard.html',account=account,len=len(account), msg = msg,am=am)
            else :
                cursor = mysql.connection.cursor()
                bn=int(0)
                all=cursor.execute('UPDATE admincustomer SET yougive=% s,pending=% s WHERE username  =% s ',( ac,bn,username))
                mysql.connection.commit()
                print(all)
                
                return render_template('customerdashboard.html',account=account,len=len(account), msg = msg,ac=ac)


            print(al)
            print(bl)      

@app.route('/customerpay',methods =['GET', 'POST'])
def customerpay():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        userid = request.form['userid']
        item = request.form['item']
        amount = request.form['amount']
        paymethod = request.form['paymethod']
        

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO customerdetails VALUES (NULL, % s, % s, % s, % s, % s)', (username,userid,item,amount,paymethod))
        mysql.connection.commit()
        
        msg = 'Added the item  successfully '
    return render_template('customerpay.html', msg = msg)
    

@app.route('/customerpayltr',methods =['GET', 'POST'])
def customerpayltr():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM customerlogin WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            cursor = mysql.connection.cursor()
            
            
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM customerdetails WHERE username  =% s ',( username,))
            account = cursor.fetchall()
            ss=len(account)
            print("Total rows are:", len(account))
            print("Printing for each row")
            print("accountdislay",account)
       
            
            return render_template('customerpayltr.html',account=account,len=len(account))
            


            
            
        else:
            msg = 'Incorrect username / password !'
    
    
       
    
    
    
            return render_template('customerlogin.html')

@app.route('/contactus', methods =['GET', 'POST'])
def contactus():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        message = request.form['message']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contactus VALUES (NULL, % s, % s, % s)', (username, email,message))
        mysql.connection.commit()
        TEXT = "Hello "+username + ",\n\n"+ """Thanks for contacting us Digital Payment Book, as soon possible early we will contact you """ 
        message  = 'Subject: {}\n\n{}'.format("Digital Payment Book", TEXT)
        #sendmail(TEXT,email)
        
        TEXTT = "Hello lokesha, Some Customer is trying to connect you, Name="+username + ",\n\n"+ """Email= """ +email+", Thanks. "
        message  = 'Subject: {}\n\n{}'.format("Digital Payment Book", TEXTT)
        #sendmail(TEXT,email)
        sendgridmail(email,TEXTT,TEXT)
        msg = 'Contact us successfully ! as soon possible we will try to contact you early'
    return render_template('contactus.html', msg = msg)
       

@app.route('/newregister', methods =['GET', 'POST'])
def newregister():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phonenumber = request.form['phonenumber']
        address = request.form['address']
        

        cursor = mysql.connection.cursor()
        print("sucess")
        cursor.execute('SELECT * FROM customerregistrationa WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO customerregistrationa VALUES (NULL, % s, % s, % s, % s,% s)', (username, email,password,phonenumber,address))
            mysql.connection.commit()
            cursor.execute('INSERT INTO customerlogin VALUES (NULL, % s, % s)', (username,password))
            mysql.connection.commit()
            yougive=int(0)
            pending=int(0)

            cursor.execute('INSERT INTO admincustomer VALUES (NULL, % s, % s, % s, % s)', (username,email,yougive,pending))
            mysql.connection.commit()
        
            msg = 'You have successfully registered !'
            TEXT = "Hello "+username + ",\n\n"+ """Thanks for applying registring at digital payment book """ 
            TEXTT = "Hello "+username + ",\n\n"+ """as registring at digital payment book """ 
            message  = 'Subject: {}\n\n{}'.format("Digital Payment Book", TEXT)
            #sendmail(TEXT,email)
            sendgridmail(email,TEXTT,TEXT)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('newregister.html', msg = msg)


@app.route('/complaintregister')
def complaintregister():
    return render_template('complaintregister.html')

@app.route('/adminsendmsgpyltr',methods =['GET', 'POST'])
def adminsendmsgpyltr():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        amount = request.form['amount']
        msg= "Message send to "+username+" Sucessfully"
        TEXT="Hi  "+username+",Lokesha from Digital Payment Book company !, I hope "+username+", your enjoying the Digital Payment Book services, I am attaching yours Pending Amount,"+amount+",as poosible soon try to clear pending Amount,Thanks"
        TEXTT="Sucessfully Sent the Pending Amount Message to the"+username+","+email+", Thanks"

        sendgridmail(email,TEXTT,TEXT)
    return render_template('adminsendmsgpyltr.html',msg=msg)

 
        

    
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port = 8080)