class RubigramError(Exception):
    def __init__(self, data: dict):
        self.status = data.get("status")
        self.message = data.get("dev_message")
        super().__init__(self.__str__())

    def __str__(self):
        return f"status={self.status}, message={self.message}"


class InvalidInput(RubigramError):
    ...


class InvalidAccess(RubigramError):
    ...


class TooRequests(RubigramError):
    ...


ERROR_MAP = {
    "INVALID_INPUT": InvalidInput,
    "INVALID_ACCESS": InvalidAccess,
    "TOO_REQUESTS": TooRequests,
}


def raise_rubigram_error(data: dict):
    error_cls = ERROR_MAP.get(data.get("status"), RubigramError)
    raise error_cls(data)