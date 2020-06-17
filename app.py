from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


class customer:
    def __init__(self, id, name, address, city, state, amount):
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.amount = amount

    def __repr__(self):
        return f"<User: {self.name}>"


users = []
users.append(User(id=1, username='Anthony', password='password'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))


Customers = []

Customers.append(customer(id='1', name='Annie',
                          address='Area1', city='Vegas', state='US', amount=1000))
Customers.append(customer(id='2', name='Reese',
                          address='Area2', city='Ohio', state='US', amount=500))
Customers.append(customer(id='3', name='Julia',
                          address='Area3', city='Atlanta', state='US', amount=900))


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users if x.username == username][0]
        except:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        if user and user.password == password:
            print("here")
            session['user_id'] = user.id
            if "Customer_Account" in request.form:
                con = sql.connect("bank.db")
                print("user1")
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO AccountExecutive_Login (username,password) VALUES (?,?)", (username, password))
                con.commit()
                con.close()
                return redirect(url_for('profile'))
            elif "Cashier" in request.form:

                con = sql.connect("bank.db")
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Cashier_Login (username,password) VALUES (?,?)", (username, password))
                con.commit()
                con.close()
                return redirect(url_for('profile2'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not g.user:
        return redirect(url_for('login'))

    elif request.method == 'POST':
        id1 = request.form['id1']
        for i in Customers:
            if id1 == i.id:
                return render_template('searchresult.html', z=[i.id, i.name, i.address, i.city, i.state, i.amount])
        flash('Customer not found please check your ID ', 'danger')
        return render_template('searchcus.html')
    return render_template('searchcus.html')


@app.route('/searchresult')
def searchresult():
    return render_template('searchresult.html')


@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@app.route('/create')
def create():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('create.html')


@app.route('/account')
def account():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('account.html')


@app.route('/delacc')
def delacc():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('delacc.html')


@app.route('/update1')
def update1():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('update1.html')


@app.route('/delcust')
def delcust():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('delcust.html')


@app.route('/update2')
def update2():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('update2.html')


@app.route('/custstatus')
def custstatus():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('custstatus.html')


@app.route('/accstatus')
def accstatus():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('accstatus.html')


@app.route('/profile2')
def profile2():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile2.html')


@app.route('/update')
def update():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('update.html')


@app.route('/getdetails')
def getdetails():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('cash-getdetails.html')


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        id1 = request.form['id1']
        amount = request.form['amount']

        for i in Customers:
            if id1 == i.id:
                i.amount += int(amount)
                flash('Deposit made successfully', 'success')
                return render_template('deposit.html')

    return render_template('deposit.html')


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        id1 = request.form['id1']
        amount = request.form['amount']

        for i in Customers:
            if id1 == i.id:
                i.amount -= int(amount)
                flash('Withdraw made successfully', 'success')
                return render_template('withdraw.html')
    return render_template('withdraw.html')


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        id1 = request.form['id1']
        id2 = request.form['id2']
        amount = request.form['amount']
        for i in Customers:
            if id1 == i.id:
                for j in Customers:
                    if id2 == j.id:
                        if i.amount < int(amount):
                            flash('User dont have sufficient money', 'success')
                            return render_template('transfer.html')        
                        i.amount -= int(amount)
                        j.amount += int(amount)
                        flash('The transfer was made successfully', 'success')
                        return render_template('transfer.html')
    return render_template('transfer.html')


@app.route('/statement')
def statement():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('statement.html')


app.run(debug=True)
