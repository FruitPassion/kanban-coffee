from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from utils.manage_config import read_config

db = SQLAlchemy()

Base = declarative_base()

config = read_config("config.txt")

association_users_teams = Table(
    "association_users_teams",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("team_id", Integer, ForeignKey("team.id"))
)

class User(UserMixin, db.Model):
    __tablename__ = "user"  # Changed to lowercase "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )
    teams = relationship(
        "Team", secondary=association_users_teams, back_populates="users"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Team(db.Model):
    __tablename__ = "team"  # Changed to lowercase "team"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(8), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )
    users = relationship(
        "User", secondary=association_users_teams, back_populates="teams"
    )

    def __repr__(self):
        return f"<Team {self.name}>"
