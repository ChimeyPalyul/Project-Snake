import inquirer
import getpass
from snake import *
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, func
from sqlalchemy.orm import Session, relationship, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()
engine = create_engine("sqlite:///players.db")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)  # Add this line
    username = Column(String, unique=True)
    password = Column(String)
    scores = relationship("Score", back_populates="user", cascade="all, delete-orphan")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    high_score = Column(Integer)
    score_history = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="scores")

def add_score(username, score):
    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()
        if user is not None:
            user_score = session.query(Score).filter(Score.user_id == user.id).first()
            if user_score is not None:
                score_history = set(user_score.score_history.split(',')) if user_score.score_history else set()  # Convert the score_history string to a set
                score_history.add(str(score))  # Add the new score to the set as a string
                user_score.score_history = ','.join(score_history)  # Convert the set back to a string
                if score > user_score.high_score:
                    user_score.high_score = score
                session.commit()
            else:
                new_score = Score(high_score=score, score_history=str(score), user_id=user.id)  # Initialize score_history as a string containing the new score
                session.add(new_score)
                session.commit()



def update_high_score(self, score):
    scores = self.scores if self.scores else []
    scores.append(score) 
    self.scores = scores
    if score > self.high_score:
        self.high_score = score

Base.metadata.create_all(engine)

def create_new_user():
    with Session(engine) as session:
        new_username = input("Enter a username: ")
        password = getpass.getpass("Enter a password: ")
        new_user = User(username=new_username, password=password)
        session.add(new_user)
        session.commit()

def delete_user(username):
    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()
        if user is not None:
            session.delete(user)
            session.commit()

def view_scores():
    with Session(engine) as session:
        scores = session.query(User.username, func.max(Score.high_score).label('max_score')).join(Score).group_by(User.username).all()
        for score in scores:
            print(f"Username: {score.username}, High Score: {score.max_score}")

def delete_all_scores():
    with Session(engine) as session:
        session.query(Score).delete()
        session.commit()



def main():
    while True:
        start = [
            inquirer.List("username",
                        message = "Select One",
                        choices = ["play game", "create new user", "delete user", "delete all scores","view the highest of scores","exit",],
                        ),
        ]
        start_response = inquirer.prompt(start)
        print(start_response)
        if start_response["username"] == "play game":
            print("Play game")
            with Session(engine) as session:
                username = input("Enter your username: ")
                user = session.query(User).filter(User.username == username).first()
                if user:
                    password = getpass.getpass("Enter your password: ")  # Prompt for password
                    if user.password == password:  # Verify password
                        game(user)
                    else:
                        print("Incorrect password")
                else:
                    print("User not found")
        elif start_response["username"] == "create new user":
            print("creating new user")
            create_new_user()
        elif start_response["username"] == "delete user":
            username = input("Enter the username of the user you want to delete: ")
            delete_user(username)
            print("user deleted")
        elif start_response["username"] == "exit":
            print("exiting program ")
            break
        elif start_response["username"] == "view the highest of scores":
            print("Viewing scores")
            view_scores()
        elif start_response["username"] == "delete all scores":
            print("Deleting all scores")
            delete_all_scores()

if __name__ == "__main__":
    main()
