#!/usr/bin/env python3
"""Build the database"""

import csv
import pathlib

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from models import User, Account

def init_db(filename: str):
    """Initialize the database"""
    this_dir = pathlib.Path(__file__).parent
    if pathlib.Path(f"{this_dir}/banking.sqlite3").exists():
        pathlib.Path(f"{this_dir}/banking.sqlite3").unlink()
    engine = sa.create_engine(f"sqlite:///{this_dir}/banking.sqlite3")
    session = scoped_session(sessionmaker(bind=engine))

    User.metadata.create_all(engine)

    with open(f"{this_dir}/{filename}.csv", "r", encoding="utf8") as f:
        content = csv.DictReader(f)
        headers = content.fieldnames
        print("CSV Headers:", headers)

        for item in content:
            try:
                user_id = item["user_id"]
            except KeyError as e:
                print(f"KeyError: {e} not found in item: {item}")
                continue

            a_user = User(
                user_id=user_id,
                user_name=item["user_name"],
                user_email=item["user_email"],
                user_password=item["user_password"],
            )
            session.add(a_user)
            
            a_account = Account(
                u_id=user_id,
                account_balance=500
            )
            session.add(a_account)

        session.commit()

def main():
    """This is the main function"""
    init_db("users")

if __name__ == "__main__":
    main()
