from __future__ import annotations

from flask_login import UserMixin

from app.models.builder import Builder


class User(UserMixin):
    """A class that represents a user of the application."""

    __slots__ = ["_is_admin"]

    def __init__(self):
        self.is_admin = False

    @property
    def is_admin(self) -> bool:
        """Gets or sets the admin status of the user.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool | None):
        """Sets the admin status of the user.

        Args:
            is_admin (bool | None): The admin status to set, or None to set it to False.
        """
        self._is_admin = False if is_admin is None else is_admin

    @staticmethod
    def create():
        """Creates a new user builder.

        Returns:
            UserBuilder: A user builder instance.
        """
        return UserBuilder()


class UserBuilder(Builder[User]):
    """A class that builds a user instance."""

    def __init__(self, user=None):
        user = user if user is not None else User()
        super().__init__(user)

    def is_admin(self, is_admin: bool | None) -> UserBuilder:
        """Sets the admin status of the user to build.

        Args:
            is_admin (bool | None): The admin status to set, or None to set it to False.

        Returns:
            UserBuilder: The same user builder instance, for method chaining.
        """
        self._item.is_admin = is_admin
        return self
