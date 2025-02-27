# -*- coding: utf-8 -*-
import logging
import os
import time
from logging import Logger
from os.path import join
from shutil import copyfile

from app.core import values
from app.core.task.stats import BenchmarkStats
from app.core.task.stats import ToolStats

_logger_error: Logger
_logger_command: Logger
_logger_main: Logger
_logger_build: Logger


def setup_logger(name, log_file, level=logging.INFO, formatter=None):
    """To setup as many loggers as you want"""
    if formatter is None:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def create_log_files():
    global _logger_main, _logger_build, _logger_command, _logger_error
    log_file_name = "log-{}".format(time.strftime("%b_%d_%H_%M"))
    log_file_path = join(values.dir_log_base, log_file_name)
    values.file_main_log = log_file_path
    _logger_main = setup_logger("main", values.file_main_log, level=logging.DEBUG)
    _logger_error = setup_logger("error", values.file_error_log)
    _logger_command = setup_logger("command", values.file_command_log)
    _logger_build = setup_logger("build", values.file_build_log)


def store_log_file(log_file_path):
    if os.path.isfile(log_file_path):
        copyfile(log_file_path, join(values.dir_logs, log_file_path.split("/")[-1]))


def store_logs():
    if os.path.isfile(values.file_main_log):
        copyfile(values.file_main_log, join(values.dir_logs, "log-latest"))
    log_file_list = [
        values.file_command_log,
        values.file_build_log,
        values.file_main_log,
        values.file_stats_log,
        values.file_error_log,
    ]
    for log_f in log_file_list:
        store_log_file(log_f)


def build(message):
    _logger_build.info(message)


def information(message):
    _logger_main.info(message)


def trace(message, info):
    pass


def command(message):
    message = str(message).strip().replace("[command]", "")
    message = "[COMMAND]: {}\n".format(message)
    _logger_main.info(message)
    _logger_command.info(message)


def docker_command(message):
    message = str(message).strip().replace("[command]", "")
    message = "[DOCKER-COMMAND]: {}\n".format(message)
    _logger_main.info(message)
    _logger_command.info(message)


def data(message, info):
    _logger_main.info(message, info)


def debug(message):
    message = str(message).strip()
    _logger_main.debug(message)


def error(message):
    _logger_main.error(message)
    _logger_error.error(message)


def note(message):
    _logger_main.info(message)


def configuration(message):
    message = str(message).strip().lower().replace("[config]", "")
    message = "[CONFIGURATION]: {}\n".format(message)
    _logger_main.info(message)


def output(message):
    message = str(message).strip()
    message = "[OUTPUT]: {}".format(message)
    _logger_main.info(message)


def warning(message):
    message = str(message).strip().lower().replace("[warning]", "")
    _logger_main.warning(message)


def log_tool_stats(task_tag_name, tool_stats: ToolStats):

    with open(values.file_stats_log, "a") as log_file:
        log_file.write("\nexperiment: {0}\n".format(task_tag_name))
        log_file.write(
            "\t\t search space size: {0}\n".format(tool_stats.patches_stats.size)
        )
        log_file.write(
            "\t\t count enumerations: {0}\n".format(
                tool_stats.patches_stats.enumerations
            )
        )
        log_file.write(
            "\t\t count plausible patches: {0}\n".format(
                tool_stats.patches_stats.plausible
            )
        )
        log_file.write(
            "\t\t count generated: {0}\n".format(tool_stats.patches_stats.generated)
        )
        log_file.write(
            "\t\t count non-compiling patches: {0}\n".format(
                tool_stats.patches_stats.non_compilable
            )
        )
        log_file.write(
            "\t\t count implausible patches: {0}\n".format(
                tool_stats.patches_stats.get_implausible()
            )
        )
        log_file.write(
            "\t\t time build: {0} seconds\n".format(tool_stats.time_stats.total_build)
        )
        log_file.write(
            "\t\t time validation: {0} seconds\n".format(
                tool_stats.time_stats.total_validation
            )
        )
        log_file.write(
            "\t\t time duration: {0} seconds\n".format(
                tool_stats.time_stats.get_duration()
            )
        )
        log_file.write(
            "\t\t latency compilation: {0} seconds\n".format(
                tool_stats.time_stats.get_latency_compilation()
            )
        )
        log_file.write(
            "\t\t latency validation: {0} seconds\n".format(
                tool_stats.time_stats.get_latency_validation()
            )
        )
        log_file.write(
            "\t\t latency plausible: {0} seconds\n".format(
                tool_stats.time_stats.get_latency_plausible()
            )
        )


def log_benchmark_stats(benchmark_tag, benchmark_stats: BenchmarkStats):

    with open(values.file_stats_log, "a") as log_file:
        log_file.write("\n benchmark bug: {0}\n".format(benchmark_tag))
        log_file.write("\t\t deployed: {0}\n".format(benchmark_stats.deployed))
        log_file.write("\t\t configured: {0}\n".format(benchmark_stats.configured))
        log_file.write("\t\t built: {0}\n".format(benchmark_stats.built))
        log_file.write("\t\t tested: {0}\n".format(benchmark_stats.tested))
