  def find_user_by(self, **kwargs) -> User:
        """ return user by filter value"""
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No results found")
            return user
        except NoResultFound:
            raise NoResultFound("No results found")
        except InvalidRequestError:
            raise InvalidRequestError("not a valid request")

    def update_user(self, user_id: int, **kwargs) -> None:
        """ a function to update the user"""
        try:
            user = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                if hasattr(user, k):
                    setattr(user, k, v)
                else:
                    raise ValueError("Such attributes do not exist")
            self._session.commit()
        except NoResultFound:
            raise NoResultFound("results not found")
