from app import db

class TableStructure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    structure = db.Column(db.Text)

    def __repr__(self):
        return '<TableStructure {}>'.format(self.name)
