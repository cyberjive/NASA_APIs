from functools import wraps
import logging
import nasa_apis.logging_config


class LogDecorator(object):
    def __init__(self):
        self.logger = logging.getLogger("NASA_Logs")

    def __str__(self):
        # return f"Logger {self.logger}"
        return "Logger %s", self.logger

    def __repr__(self):
        return f"{self.__class__.__name__}"  # f"{self.logger!r}"

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug(
                    # f"Function: {func.__name__}", f"Args: {args}", f"Kwargs: {kwargs}"
<<<<<<< HEAD
<<<<<<< HEAD
                    """Function: %s
=======
                    """Function: %s"
>>>>>>> 0ea9c0eff3e1361f3dc26e8e9aafea12dc3e6186
=======
                    """Function: %s"
>>>>>>> 0ea9c0eff3e1361f3dc26e8e9aafea12dc3e6186
                    Args: %s
                    Kwargs: %s
                    """
                    % (func.__name__, args, kwargs)
                )
                ret = func(*args, **kwargs)
                self.logger.debug("Result: %s" % ret)
                return ret
            except Exception as e:
                self.logger.debug("Exception %s" % e)
                raise e

        return wrapper