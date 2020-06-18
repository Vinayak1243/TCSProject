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
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from datetime import date

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer)
    name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    add1 = db.Column(db.String(200))
    add2 = db.Column(db.String(200))

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
        self.activity = []

    def __repr__(self):
        return f"<User: {self.name}>"


class cust:
    def __init__(self, sid, cid, status, message, update):
        self.sid = sid
        self.cid = cid
        self.status = status
        self.message = message
        self.update = update

    def __repr__(self):
        return f"<User: {self.status}>"


class acc:
    def __init__(self, cid, aid, type1, status, message, update, amount):
        self.cid = cid
        self.aid = aid
        self.type1 = type1
        self.status = status
        self.message = message
        self.update = update
        self.amount = amount

    def __repr__(self):
        return f"<User: {self.cid}>"


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

Cust = []

Cust.append(cust(sid='1', cid='1', status='active',
                 message='none', update='recently'))
Cust.append(cust(sid='2', cid='2', status='inactive',
                 message='none', update='recently'))
Cust.append(cust(sid='3', cid='3', status='active',
                 message='none', update='many months ago'))

Acc = []

Acc.append(acc(cid='1', aid='1', amount=400, type1='Savings Account',
               status='active', message='none', update='recently'))
Acc.append(acc(cid='2', aid='2', amount=500, type1='Current Account',
               status='inactive', message='none', update='recently'))
Acc.append(acc(cid='3', aid='3', amount=300, type1='Savings Account',
               status='active', message='none', update='many months ago'))


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


@app.route('/account', methods=['GET', 'POST'])
def account():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        try:
            id1 = request.form['cid']
            amount = request.form['amount']
            type1 = request.form['type1']
            a = date.today()
            for i in Customers:
                if i.id == id1:
                    Acc.append(acc(cid=id1, aid=None, amount=amount, type1=type1,
                                   status='active', message=None, update=a))
                    flash('Account created successfully', 'success')
                    return render_template('account.html')
            flash('No account found with this id', 'danger')
            return render_template('account.html')
        except:
            flash('Enter all the details', 'danger')
            return render_template('account.html')

    return render_template('account.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        cid = request.form['cid']
        for i in Customers:
            if i.id == cid:
                flash('Invalid customer ID', 'warning')
                return render_template('create.html')
        name = request.form['name']
        address = request.form['add1']+' ' + request.form['add2']
        city = request.form['city']
        state = request.form['state']

        Customers.append(customer(id=cid, name=name,
                                  address=address, city=city, state=state, amount=0))
        Cust.append(cust(sid=1, cid=cid, status='active',
                         message='none', update='today'))
        flash('Customer details created successfully', 'success')
        return render_template('create.html')

    return render_template('create.html')


@app.route('/delacc', methods=['GET', 'POST'])
def delacc():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        id1 = request.form['id1']
        type1 = request.form['type1']
        for i in Acc:
            if id1 == i.cid and type1 == i.type1:
                Acc.remove(i)
                flash('Account deleted successfully', 'success')
                return render_template('delacc.html')

        flash('Account not found', 'danger')

    return render_template('delacc.html')


@app.route('/update1', methods=['GET', 'POST'])
def update1():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        cid = request.form['cid']
        for i in Customers:
            if i.id == cid:
                flash('Customer Id Found ', "success")
                return redirect(url_for('update2'))
        flash('Customer Id invalid', 'danger')
    return render_template('update1.html')


@app.route('/delcust', methods=['GET', 'POST'])
def delcust():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        cid = request.form['cid']
        name = request.form['name']
        for i in Customers:
            if cid == i.id and name == i.name:
                Customers.remove(i)
                for i in Cust:
                    if cid == i.cid:
                        Cust.remove(i)
                flash('Customer details deleted successfully', 'success')
                return render_template('delcust.html')

        flash('No Customer Found Check your details', 'danger')

    return render_template('delcust.html')


@app.route('/update2', methods=['GET', 'POST'])
def update2():
    if not g.user:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        cid = request.form['cid']
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        for i in Customers:
            if cid == i.id:
                i.id = cid
                i.name = name
                i.address = address
                i.city = city
                i.state = state
                flash('Customer details updated successfully', 'success')
                return render_template('update1.html')
    return render_template('update2.html')


@app.route('/custstatus')
def custstatus():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('custstatus.html', z=Cust)


@app.route('/accstatus')
def accstatus():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('accstatus.html', z=Acc)


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
                s = date.today()
                i.amount += int(amount)
                i.activity.append(
                    [len(i.activity)+1, s, 'Debit', amount, i.amount])
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
            s = date.today()
            if id1 == i.id:
                i.amount -= int(amount)
                i.activity.append(
                    [len(i.activity)+1, s, 'Credit', amount, i.amount])
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
                        s = date.today()
                        i.activity.append(
                            [len(i.activity)+1, s, 'Credit', amount, i.amount])
                        j.activity.append(
                            [len(i.activity)+1, s, 'Debit', amount, j.amount])
                        flash('The transfer was made successfully', 'success')
                        return render_template('transfer.html')
    return render_template('transfer.html')


@app.route('/statement', methods=['GET', 'POST'])
def statement():
    if not g.user:
        return redirect(url_for('login'))

    elif request.method == 'POST':
        id1 = request.form['id1']
        for i in Customers:
            if id1 == i.id:
                return render_template('statementresult.html', z=i.activity)
    return render_template('statement.html')


app.run(debug=True)
