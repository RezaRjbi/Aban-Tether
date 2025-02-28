from django.core.cache import cache
import time
from typing import Final


class OTP:
    def __init__(self, identifier: str) -> None:
        self.identifier: Final[str] = identifier
        self.otp_timeout: Final[int] = 120

    def send(self, identifier: str, otp: str = "123456") -> bool:
        otp_data = {"otp": otp, "ts": time.time()}
        return cache.add(identifier, otp_data, self.otp_timeout)

    def verify(self, identifier: str, otp: str = "123456") -> bool:
        sent_otp = cache.get(self.identifier)
        return sent_otp is not None and sent_otp["otp"] == otp
