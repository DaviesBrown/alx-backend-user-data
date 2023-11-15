#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """ save user to db"""
        user = User(email=email, hashed_password=hashed_password)
        if email is None and hashed_password is None:
            return None
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwd) -> User:
        """ find user by keyword arg"""
        session = self._session
        for k in kwd:
            if k not in User.__class__.columns:
                raise InvalidRequestError()
        user = session.query(User).filter_by(**kwd).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: str, **kwd) -> None:
        """ updates user's atribute"""
        if user_id is None:
            return
        user = self.find_user_by(id=user_id)
        for k, v in kwd.items():
            setattr(user, k, v)
        self._session.commit()
