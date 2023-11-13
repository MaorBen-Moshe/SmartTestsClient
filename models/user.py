from __future__ import annotations

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self):
        self.is_admin = False

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool | None):
        self._is_admin = False if is_admin is None else is_admin


class UserBuilder:
    def __init__(self):
        self._user = User()

    def build(self) -> User:
        return self._user

    def is_admin(self, is_admin: bool | None) -> UserBuilder:
        self._user.is_admin = is_admin
        return self
