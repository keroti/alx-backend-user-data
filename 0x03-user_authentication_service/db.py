#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        and return The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided keyword args
        and return The first User object that matches the
        filtering conditions or raise error
        """
        users = self._session.query(User)
        for i, j in kwargs.items():
            if i not in User.__dict__:
                raise InvalidRequestError
            for usr in users:
                if getattr(usr, i) == j:
                    return usr
        raise NoResultFound
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes and
        raise ValueError if an invalid attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
            for attr, value in kwargs.items():
                if hasattr(user, attr):
                    setattr(user, attr, value)
                else:
                    raise ValueError(f"Invalid attribute: {attr}")
            self._session.commit()
        except NoResultFound:
            raise ValueError("User not found")