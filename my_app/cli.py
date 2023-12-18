import click
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, DogBreed, UserVote
from database import SessionLocal, engine

@click.group()
def cli():
    pass

@cli.command()
@click.argument('username', type=str)
@click.argument('email', type=str)
@click.argument('password', type=str)
def register(username, email, password):
    """Command to register a new user."""
    try:
        # Create a session
        db = SessionLocal()

        # Check if the username or email already exists
        if db.query(User).filter((User.user_name == username) | (User.email == email)).first():
            click.echo("Username or email already exists. Please choose a different one.")
        else:
            # Create a new user
            new_user = User(user_name=username, email=email, password=password, vote_credits=5)

            # Add the user to the session
            db.add(new_user)

            # Commit the changes
            db.commit()

            click.echo(f"User {username} registered successfully.")
    except IntegrityError as e:
        click.echo(f"IntegrityError: {str(e)}")
        click.echo("Error: Email already exists. Please choose a different one.")
    finally:
        # Close the session
        db.close()

@cli.command()
@click.argument('username', type=str)
@click.argument('password', type=str)
def login(username, password):
    """Command to log in as a user."""
    try:
        # Create a session
        db = SessionLocal()

        # Check if the username and password match
        user = db.query(User).filter((User.user_name == username) & (User.password == password)).first()

        if user:
            click.echo(f"Welcome, {username}! You are now logged in.")
        else:
            click.echo("Invalid username or password. Please try again.")
    finally:
        # Close the session
        db.close()

# ...
@cli.command()
@click.argument('name', type=str)
@click.argument('description', type=str)
def add_breed(name, description):
    try:
        # Create a session
        db = SessionLocal()

        # Generate a unique breed_id (you can use a function to generate unique IDs)
        # For simplicity, let's use a basic incrementing integer as an example
        new_breed_id = str(db.query(DogBreed).count() + 1)

        # Insert the new dog breed
        new_breed = DogBreed(breed_id=new_breed_id, name=name, description=description, average_rating=0)
        db.add(new_breed)
        db.commit()

        click.echo(f"Dog breed '{name}' added successfully with ID: {new_breed_id}")

    finally:
        # Close the session
        db.close()



@cli.command()
@click.argument('breed_id', type=str)
def remove_breed(breed_id):
    """Command to remove a dog breed."""
    try:
        # Create a session
        db = SessionLocal()

        # Check if the breed exists
        breed = db.query(DogBreed).filter(DogBreed.breed_id == breed_id).first()

        if breed:
            # Remove the breed from the session
            db.delete(breed)

            # Commit the changes
            db.commit()

            click.echo(f"Dog breed {breed_id} removed successfully.")
        else:
            click.echo("Dog breed not found.")
    finally:
        # Close the session
        db.close()

@cli.command()
def list_breeds():
    """Command to list all dog breeds from the database."""
    try:
        # Create a session
        db = SessionLocal()

        # Query all dog breeds
        breeds = db.query(DogBreed).all()

        # Display breed information
        for breed in breeds:
            click.echo(f"Breed ID: {breed.breed_id}, Name: {breed.name}, Description: {breed.description}")

    finally:
        # Close the session
        db.close()

@cli.command()
@click.argument('user_id', type=int)
@click.argument('breed_id', type=str)
@click.argument('vote_type', type=str)
def vote(user_id, breed_id, vote_type):
    """Command to add a vote (upvote or downvote) for a user and a dog breed."""
    try:
        # Create a session
        db = SessionLocal()

        # Check if user and breed exist
        user = db.query(User).filter(User.user_id == user_id).first()
        breed = db.query(DogBreed).filter(DogBreed.breed_id == breed_id).first()

        if user and breed:
            # Check if the user has enough vote credits
            if user.vote_credits > 0:
                # Create a UserVote instance
                new_vote = UserVote(user_id=user_id, breed_id=breed_id, vote_type=vote_type)

                # Add the vote to the session
                db.add(new_vote)

                # Update user's vote credits and breed's average rating
                user.vote_credits -= 1
                breed.average_rating = calculate_average_rating(breed)

                # Commit the changes
                db.commit()

                click.echo(f"Vote added successfully for User ID {user_id} on Dog Breed ID {breed_id}.")
                click.echo(f"Remaining vote credits for {user.user_name}: {user.vote_credits}")
            else:
                click.echo("Insufficient vote credits. Earn more credits by voting on other breeds.")
        else:
            click.echo("User or breed not found.")

    finally:
        # Close the session
        db.close()

def calculate_average_rating(breed):
    """Calculate the average rating for a dog breed."""
    votes = breed.votes
    total_votes = len(votes)
    if total_votes > 0:
        sum_ratings = sum([1 if vote.vote_type == 'upvote' else -1 for vote in votes])
        average_rating = sum_ratings / total_votes
        return round(average_rating, 2)
    else:
        return 0.0


if __name__ == "__main__":
    cli()
