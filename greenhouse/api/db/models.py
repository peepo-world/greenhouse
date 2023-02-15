from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Emote(Base):
    __tablename__ = "emote"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    access = Column(Boolean)

    # Columns to add:
    image = Column(LargeBinary)
    # Probably child classes or some other relationship for variants

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    user_name = Column(String(50), nullable=False, unique=True)
    twitch_id = Column(String(12), nullable=False, unique=True)
    profile = relationship("Profile", back_populates="owner")

    # Add creation time, maybe if they're active? Idk

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    pronouns = Column(String(20))
    bio = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="profile")

    # Columns to add:
    #profile_pic = Column(LargeBinary)