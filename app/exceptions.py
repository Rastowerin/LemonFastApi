class BadRequestException(Exception):
    @property
    def status(self):
        raise NotImplemented
