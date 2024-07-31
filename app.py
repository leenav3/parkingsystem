import mysql.connector
from flask import Flask,request,render_template,redirect,url_for, session
import re

app = Flask(__name__)
app.secret_key = "nurav"
conn = mysql.connector.connect(host = 'localhost',user= 'root',password= 'nps@1234',database= 'parking_system') 
cursor = conn.cursor()

@app.route('/')
def index():
    #home page showing available spots
    conn = mysql.connector.connect(host = 'localhost',user= 'root',password= 'nps@1234',database= 'parking_system')
    cursor = conn.cursor()
    cursor.execute('Select spot_id from parking_spots where status = "available"')
    data = cursor.fetchall()
    
    #print("Available spots", list(data))
    return render_template('home.html',available_spots =data)
    

@app.route('/book_spot', methods=['POST'])
def book_spot():
    #accepting user input 
    if request.method =='POST':
        spot_id = request.form['spot_id']
        date_time = request.form['date_time']
    
    conn = mysql.connector.connect(host = 'localhost',user= 'root',password= 'nps@1234',database= 'parking_system')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM parking_spots WHERE spot_id = %s", (spot_id,))
    result = cursor.fetchone()
    cursor.reset()
    
    
    if result:
        
        cursor.execute("UPDATE parking_spots SET status = 'booked', booking_time = %s WHERE spot_id = %s", (date_time, spot_id,))
        conn.commit()
        message = 'Spot booked successfully!'
        cursor.reset()
    else:
        message = 'Spot is occupied or not found'
        
    return render_template('book_spot.html',message=message)
@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = mysql.connector.connect(host = 'localhost',user= 'root',password= 'nps@1234',database= 'parking_system')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM accounts WHERE email = %s', (email, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            #session['id'] = account['ID']
            #session['user'] = account['email']
            #session['firstname']=account['firstName']
            
            msg = 'Logged in successfully !'
            print(msg)
            print(session)
            return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

        

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['firstName']
        password = request.form['password1']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postal_code']
        conn = mysql.connector.connect(host = 'localhost',user= 'root',password= 'nps@1234',database= 'parking_system')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM accounts WHERE email = %s', (email, ))
        account = cursor.fetchone()
     
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts(username, password, email, city, state, country, postalcode) VALUES \
            ( %s, %s, %s, %s, %s, %s, %s)',
                           (username, password, email, city, state, country, postalcode, ))

            conn.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'GET':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)
 
    
if __name__ == '__main__':
    app.run(debug=True)

cursor.close()
conn.close()

