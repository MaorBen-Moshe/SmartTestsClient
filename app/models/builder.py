from typing import Any


class Builder:
    def __init__(self, item: Any):
        self.item = item

    def build(self) -> Any:
        return self.item
