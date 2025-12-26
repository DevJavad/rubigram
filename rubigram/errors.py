class InvalidInput(Exception):
    def __init__(self, data: dict):
        self.status = data.get("status")
        self.message = data.get("dev_message")

    def __str__(self):
        return f"InvalidInputError(status={self.status}), message={self.message}"


class InvalidAccess(Exception):
    def __init__(self, data: dict):
        self.status = data.get("status")
        self.message = data.get("dev_message")

    def __str__(self):
        return f"InvalidAccessError(status={self.status}), message={self.message}"