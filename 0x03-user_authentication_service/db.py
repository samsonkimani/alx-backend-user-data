"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError
from user import User
from user import Base
from typing import Mapping, TypeVar


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

        # new_user = User(
        #     email=email,
        #     hashed_password=hashed_password,
        #     session_id='',
        #     reset_token='')
        # self._session.add(new_user)

        # try:
        #     self._session.commit()
        #     return new_user
        # except SQLAlchemyError as e:
        #     self._session.rollback()
        #     raise e
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    # def find_user_by(self, **kwargs: Mapping) -> User:
    #     """ return user by filter value"""
    #     try:
    #         user = self._session.query(User).filter_by(**kwargs).first()
    #         if user is None:
    #             raise NoResultFound("No results found")
    #         return user
    #     except NoResultFound:
    #         raise NoResultFound("No results found")
    #     except InvalidRequestError:
    #         raise InvalidRequestError("not a valid request")

    # def update_user(self, user_id: str, **kwargs: dict[str, str]) -> None:
    #     """ a function to update the user"""
    #     try:
    #         user = self.find_user_by(id=user_id)
    #         for k, v in kwargs.items():
    #             if hasattr(user, k):
    #                 setattr(user, k, v)
    #             else:
    #                 raise ValueError("Such attributes do not exist")
    #         self._session.commit()
    #     except NoResultFound:
    #         raise NoResultFound("results not found")
