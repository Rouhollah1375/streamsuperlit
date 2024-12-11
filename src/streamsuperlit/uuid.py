import uuid

class UUID:
    def __init__(self) -> None:
        self._generated_uuids = []

    def get_uuid(self):
        id = uuid.uuid4().hex
        self._generated_uuids.append(id)
        return id