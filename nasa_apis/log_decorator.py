from functools import wraps
import logging


class LogDecorator(object):
    def __init__(self):
        self.logger = logging.getLogger("NASA_Logs")

    def __str__(self):
        return f"Logger {self.logger}"

    def __repr__(self):
        return f"{self.__class__.__name__}" f"{self.logger!r}"

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug(
                    f"Function: {func.__name__}," f"Args: {args}", f"Kwargs: {kwargs}"
                )
                ret = func(*args, **kwargs)
                self.logger.debug(f"Result {ret}")
                return ret
            except Exception as e:
                self.logger.debug(f"Exeception {e}")
                raise e
            return ret

        return wrapper