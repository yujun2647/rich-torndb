import os
import sys
import logging
import functools
from rich_torndb.utils.printer import to_pretty_string


def get_log_path(_file_):
    dir_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    dir_path = os.path.join(dir_path, "logs", "rich-torndb")
    os.makedirs(dir_path, exist_ok=True)
    file = os.path.basename(_file_)
    log_filename = f"{file[:file.rindex('.')]}.log"
    return os.path.join(dir_path, log_filename)


def set_scripts_logging(_file_, level=logging.INFO):
    """
        为了是脚本log安装正确，请把此函数的调用放在脚本的最上面， 例：
            from commons import set_scripts_logging
            set_scripts_logging(__file__)

            import logging
            import ..others..

    @_file_:
    @level:
    @return:
    """

    log_filename = get_log_path(_file_)
    logger = logging.getLogger()
    if logger.handlers:  # 防止多个脚本都调用此函数时，且脚本间存在互掉的情况下，覆盖 io_handler
        return
    logging.basicConfig(level=level,
                        format=("%(asctime)s %(filename)s "
                                "[line:%(lineno)d] %(levelname)s %(message)s"),
                        datefmt="%a, %d %b %Y %H:%M:%S",
                        filename=log_filename)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s"))
    logger.addHandler(console_handler)
    logging.info("\nLog_filename: {}".format(log_filename))
    return log_filename


LOG_LEVEL_METHOD_MAP = {
    logging.INFO: logging.info,
    logging.DEBUG: logging.debug,
    logging.WARNING: logging.warning,
    logging.ERROR: logging.ERROR
}


def log_return(desc="", level=logging.INFO, front="", end=""):
    def out_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            log_method = LOG_LEVEL_METHOD_MAP.get(level, logging.INFO)
            log_method(f"{front}{desc}{to_pretty_string(result)}{end}")
            return result

        return wrapper

    return out_wrapper


@log_return("测试: ")
def test(a, b):
    return dict(a=a, b=b)


if __name__ == "__main__":
    set_scripts_logging(__file__)
    test(1, 2)
