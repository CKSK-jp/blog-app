import dbm

from app import app

with app.test_request_context():
    dbm.session.execute("SELECT * FROM songs").fetchall()
