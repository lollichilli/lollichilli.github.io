from flask import redirect, render_template, request, url_for, session
from config import app, db
from models import User, Account, Transaction
from datetime import datetime

# Home Page
@app.route('/')
def index():
    # Check if the user is already in session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else :
        # Get the user id from session
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        username = user.user_name
        email = user.user_email
        account = Account.query.filter_by(u_id=user_id).first()
        balance = account.account_balance
        return render_template('index.html', username=username, email=email,
        balance=balance)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the login info from the form and query it from User
        loginForm = request.form
        useremail = loginForm['useremail']
        password = loginForm['password']
        currentUser = User.query.filter_by(user_email=useremail).first()
        # Check if valid and then redirect user accordingly
        if (currentUser) :
            if (currentUser.user_password == password) :
                session['user_id'] = currentUser.user_id
                return redirect(url_for('index'))
            else :
                return "Incorrect Password"
        else :
            return "Account doesn't exist"
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the registration form info
        registrationForm = request.form
        # Check if the user already exists
        user = User.query.filter_by(user_name=registrationForm['username']).first()
        email = User.query.filter_by(user_email=registrationForm['email']).first()
        if (user and email) :
            return "Username or Email Already Exist"
        elif (user) :
            return "Username Already Exists"
        elif (email) :
            return "Email Already Exists"
        else :
            # Create a new user
            newUser = User(
                user_name = registrationForm['username'],
                user_email = registrationForm['email'],
                user_password = registrationForm['password']
            )
            # Add the new user to the database
            db.session.add(newUser)
            db.session.commit()
            # Initialize the account balance
            newAccount = Account(
                u_id = newUser.user_id,
                account_balance = 0
            )
            db.session.add(newAccount)
            db.session.commit()
            # Store the user in session
            session['user_id'] = newUser.user_id
            # Redirect to the home page with the user parameter updated
            return redirect(url_for('index'))
    return render_template('register.html')

# Transaction view
@app.route('/transactions', methods=['GET', 'POST'])
def transaction_history():
    # Verify that user is logged in
    if 'user_id' not in session:
        return redirect(url_for('index', user=None))
    # Get the user id from session
    user_id = session['user_id']
    # Get the users account id
    account_id = Account.query.filter_by(u_id=user_id).first().account_id
    # Get the users transactions from the account id
    transactions_from_user = Transaction.query.filter_by(from_account_id=account_id).order_by(Transaction.transaction_date)
    # Get the transactions to the user
    transactions_to_user = Transaction.query.filter_by(to_account_id=account_id).order_by(Transaction.transaction_date)

    # Context
    context = {
        'User': User,
        'Account': Account
    }

    # Render the template with the users transaction history
    return render_template(
        'transaction_history.html',
        transactions_from_user=transactions_from_user,
        transactions_to_user=transactions_to_user,
        **context
        )

@app.route('/send', methods=['GET', 'POST'])
def send_money():
    # Verify that user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Get the user id from session
    user_id = session['user_id']

    if request.method == 'POST':
        # Get the send money form info
        moneyForm = request.form

        # Update the users balances
        to_user = User.query.filter_by(user_name=moneyForm['username']).first()
        to_user_id = to_user.user_id
        from_account = Account.query.filter_by(u_id=user_id).first()
        to_account = Account.query.filter_by(u_id=to_user_id).first()
        amount = float(moneyForm['amount'])
        from_account_new_balance = from_account.account_balance - amount
        to_account_new_balance = to_account.account_balance + amount
        from_account.account_balance = from_account_new_balance
        db.session.commit()
        to_account.account_balance = to_account_new_balance
        db.session.commit()

        # Record the transaction
        newTransaction = Transaction(
            transaction_date = datetime.now(),
            from_account_id = from_account.account_id,
            to_account_id = to_account.account_id,
            amount = amount
        )

        # Add the transaction to database
        db.session.add(newTransaction)
        db.session.commit()

        return redirect(url_for('index'))

    
    # Render the template with the users transaction history
    return render_template(
        'send_money.html'
        )
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the session
    session.pop('user_id', None)
    # Redirect to the login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()