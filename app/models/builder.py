from typing import TypeVar, Generic

T = TypeVar("T")


class Builder(Generic[T]):
    """A generic class that builds an item of type T."""

    __slots__ = ["_item"]

    def __init__(self, item: T):
        """Initializes the builder with an item of type T.

        Args:
            item (T): The item to build.
        """
        self._item = item

    def build(self) -> T:
        """Returns the built item of type T.

        Returns:
            T: The built item.
        """
        return self._item
