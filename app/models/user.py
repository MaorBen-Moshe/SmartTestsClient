from __future__ import annotations

from flask_login import UserMixin

from app.models.builder import Builder


class User(UserMixin):
    def __init__(self):
        self.is_admin = False

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool | None):
        self._is_admin = False if is_admin is None else is_admin

    @staticmethod
    def create():
        return UserBuilder()


class UserBuilder(Builder[User]):
    def __init__(self, user=None):
        user = user if user is not None else User()
        super().__init__(user)

    def is_admin(self, is_admin: bool | None) -> UserBuilder:
        self.item.is_admin = is_admin
        return self
