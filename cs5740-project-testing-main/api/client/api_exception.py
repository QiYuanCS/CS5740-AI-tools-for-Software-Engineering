class ApiException(Exception):
    def __init__(self, status_code, detail=None, traceback=None):
        default_detail = "No detail provided."
        default_traceback = "No traceback provided."

        super().__init__(f"API Error: Status Code {status_code}, Detail: {detail or default_detail}")

        self.status_code = status_code
        self.detail = detail or default_detail
        self.traceback = traceback or default_traceback
