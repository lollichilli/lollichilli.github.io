#!/usr/bin/env python3
"""Models"""

from config import db, ma

class User(db.Model):
    """User class"""

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True) 
    user_name = db.Column(db.String(50), nullable=False) 
    user_email = db.Column(db.String(50), nullable=False) 
    user_password = db.Column(db.String(50), nullable=False) 

class Account(db.Model):
    """Account class"""

    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    account_balance = db.Column(db.Integer, nullable=False) 

class Transaction(db.Model):
    """Transaction class"""
  
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, nullable=False)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)  
    amount = db.Column(db.Integer, nullable=False)

    

class UserSchema(ma.SQLAlchemySchema):
    """User schema"""

    class Meta:
        """User metadata"""

        model = User
        load_instance = True

    user_id = ma.auto_field()
    user_name = ma.auto_field()
    user_email = ma.auto_field()
    user_password = ma.auto_field()

class AccountSchema(ma.SQLAlchemySchema):
    """Account schema"""

    class Meta:
        """Account metadata"""

        model = Account
        load_instance = True

    account_id = ma.auto_field()
    u_id = ma.auto_field()
    account_balance = ma.auto_field()

class TransactionSchema(ma.SQLAlchemySchema):
    """Transaction schema"""

    class Meta:
        """Transaction metadata"""

        model = Transaction
        load_instance = True

    transaction_id = ma.auto_field()
    transaction_date = ma.auto_field()
    from_account_id = ma.auto_field()
    to_account_id = ma.auto_field()
    amount = ma.auto_field()