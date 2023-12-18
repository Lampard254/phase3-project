from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(50))
    vote_credits = Column(Integer)

    # Define a relationship to the UserVote class
    votes = relationship('UserVote', back_populates='user')

class DogBreed(Base):
    __tablename__ = 'Dog_breed'

    breed_id = Column(String(50), primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    average_rating = Column(Integer)
    votes = relationship('UserVote', back_populates='breed')

class UserVote(Base):
    __tablename__ = 'User_vote'

    vote_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    breed_id = Column(String(50), ForeignKey('Dog_breed.breed_id'))
    vote_type = Column(String(50))

    # Define a relationship to the User class
    user = relationship('User', back_populates='votes')
    breed = relationship('DogBreed', back_populates='votes')
