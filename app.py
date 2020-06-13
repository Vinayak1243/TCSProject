from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='Anthony', password='password'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))


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

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')


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
    else:
        return render_template('Profile2.html')
@app.route('/getdetails')
def getdetails():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('cash-getdetails.html')

app.run(debug=True)    
