"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base
from typing import TypeVar


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
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """ method to add a user to a database"""
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except:
            return None

    def find_user_by(self, **kwargs):
        """ return user by filter value"""
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No results found")
            return user
        except InvalidRequestError:
            raise InvalidRequestError("not a valid request")
        return
    def update_user(self, user_id, **kwargs):
        """ a function to update the user"""
        try:
            user = self.find_user_by(user_id)
            if user is not None:
                for k, v in kwargs.items():
                    user.k = v
                self._session.commit()
            return None
        except ValueError:
            return
