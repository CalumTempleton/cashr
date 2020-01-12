from app import db


class Transactions(db.Model):
    """This class represents the transactions table."""

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255))
    balance = db.Column(db.Float)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, date, description, category, balance, value):
        # Initialise class
        self.date = date
        self.description = description
        self.category = category
        self.balance = balance
        self.value = value

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Transactions.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_by(description):
        return Transactions.query.filter_by(description=description).all()

    def __repr__(self):
        return "<Transactions: {}>".format(self.description)
