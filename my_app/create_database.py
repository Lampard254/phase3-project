# create_database.py

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./my_database.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Update User class in create_database.py
class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(50))
    vote_credits = Column(Integer)
    votes = relationship('UserVote', back_populates='user')

# Dog Breed Table
class DogBreed(Base):
    __tablename__ = 'Dog_breed'

    breed_id = Column(String(50), primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    average_rating = Column(Integer)
    votes = relationship('UserVote', back_populates='breed')

# User Vote Table
class UserVote(Base):
    __tablename__ = 'User_vote'

    vote_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    breed_id = Column(String(50), ForeignKey('Dog_breed.breed_id'))
    vote_type = Column(String(50))

    user = relationship('User', back_populates='votes')
    breed = relationship('DogBreed', back_populates='votes')



Base.metadata.create_all(bind=engine)

# Insert sample data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Insert users
user1 = User(user_name="Alice", email="alice@email.com", password="hashed123", vote_credits=5)
user2 = User(user_name="Bob", email="bob@email.com", password="hashed456", vote_credits=3)
user3 = User(user_name="Charlie", email="charlie@email.com", password="hashed789", vote_credits=10)

session.add_all([user1, user2, user3])
session.commit()

# Insert dog breeds
breed1 = DogBreed(breed_id="101", name="Golden Retriever", description="Friendly and intelligent", average_rating=4)
breed2 = DogBreed(breed_id="102", name="Labrador", description="Outgoing and even-tempered", average_rating=4.5)
breed3 = DogBreed(breed_id="103", name="Beagle", description="Curious and friendly", average_rating=3.8)

session.add_all([breed1, breed2, breed3])
session.commit()

# Insert user votes
# Insert user votes
vote1 = UserVote(user_id=1, breed_id="101", vote_type="upvote")
vote2 = UserVote(user_id=2, breed_id="102", vote_type="upvote")
vote3 = UserVote(user_id=3, breed_id="103", vote_type="downvote")
vote4 = UserVote(user_id=1, breed_id="102", vote_type="downvote")
vote5 = UserVote(user_id=2, breed_id="101", vote_type="upvote")

session.add_all([vote1, vote2, vote3, vote4, vote5])
session.commit()


print("Sample data inserted successfully.")
