from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add users
rain = User(first_name='Rain', last_name='Babauta')
shweta = User(first_name='Shweta', last_name='Hosamani')
joel = User(first_name='William', last_name='Burton')

db.session.add(rain)
db.session.add(shweta)
db.session.add(joel)

db.session.commit()
