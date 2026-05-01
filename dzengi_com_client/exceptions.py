class DzengiException(Exception):
    pass


class DzengiAPIException(DzengiException):
    def __init__(self, response):
        self.status_code = response.status_code
        try:
            json_res = response.json()
        except Exception:
            json_res = {}
        self.code = json_res.get("code", None)
        self.message = json_res.get("msg", "Unknown error")
        super().__init__(f"[{self.status_code}] code={self.code}: {self.message}")


class DzengiRequestException(DzengiException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
