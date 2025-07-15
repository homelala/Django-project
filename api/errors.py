from rest_framework.exceptions import APIException

class RedisLockConflictException(APIException):
    def __init__(self, message, code):
        self.status_code = code
        self.detail = message
        self.default_code = "redis_lock_conflict"