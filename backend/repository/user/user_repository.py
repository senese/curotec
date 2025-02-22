from entities.entities import User
from ..base_repository import BaseRepository
from ..user.user_model import UserModel
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from typing import List


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def insert(self, entity: User) -> UserModel:
        user_dict = entity.model_dump(mode="json")
        new_user = UserModel(**user_dict)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, entity: User) -> UserModel:
        user = self.find_by_email(entity.email)
        user.name = entity.name
        self.session.commit()
        return user

    def find(self, id: int) -> UserModel:
        try:
            user = self.session.query(UserModel).filter_by(id=id).one()
        except NoResultFound:
            raise NoResultFound("User not found")
        return user

    def find_by_email(self, email: str) -> UserModel:
        try:
            user = self.session.query(UserModel).filter_by(email=email).one()
        except NoResultFound:
            raise NoResultFound("User not found")
        return user

    def find_all(self) -> List[UserModel]:
        return self.session.query(UserModel).all()

    def delete(self, user: UserModel) -> None:
        self.session.delete(user)
        self.session.commit()
