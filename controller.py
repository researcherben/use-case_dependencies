#!/usr/bin/env python3

# Ben Payne, 2021
# https://creativecommons.org/licenses/by/4.0/
# Attribution 4.0 International (CC BY 4.0)

"""
"""

import os
import json

# https://realpython.com/python-logging-source-code/
import argparse  # https://docs.python.org/3.3/library/argparse.html

# https://docs.python.org/3/howto/logging.html
import logging

# https://gist.github.com/ibeex/3257877
from logging.handlers import RotatingFileHandler


# need "pip install pygraphviz"
# which requires a local installation of graphviz
from pygraphviz import AGraph

# https://pygraphviz.github.io/documentation/stable/tutorial.html
# https://pygraphviz.github.io/documentation/latest/reference/agraph.html
import random
from typing import Tuple


def write_to_file(folder_name: str, this_dict: dict, this_prefix: str) -> None:
    """
    >>> write_to_file()
    """
    with open(
        folder_name + "/" + this_prefix + this_dict["short name"] + ".json", "w"
    ) as file_handle:
        json.dump(this_dict, file_handle, indent=2)
    return

def args_parser():
    theparser = argparse.ArgumentParser(description="generate Graphviz of use cases and user stories from JSON", allow_abbrev=False)

    theparser.add_argument(
        "--input_filename",
        metavar="<filename>",
        type=str,
        default="use_cases_and_user_stories_and_acceptance_tests.json",
        help="Name of input JSON file",
    )

    theparser.add_argument(
        "--no_output",
        action="store_true",
        help="do not create files"
    )
    # even though this script is under version control in a git repo,
    # the --version is useful for when the code base is provided to
    # a user outside of git
    theparser.add_argument(
        "--version", action="store_true", help="version of this script"
    )
    # https://semver.org/
    # MAJOR version when you make incompatible API changes,
    # MINOR version when you add functionality in a backwards compatible manner, and
    # PATCH version when you make backwards compatible bug fixes.

    return theparser.parse_args()


if __name__ == "__main__":

    args = args_parser()
    #print(args)

    if args.version:
        print("version: 1.0")
        exit(0)

    # TODO: the color of testable nodes should be set by the result of the test
    # TODO: the color of top-level non-testable nodes should be set based on the color of lower nodes

    if args.no_output:
        create_files =False
    else:
        create_files = True

    folder_name = "output"
    if create_files:
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

    with open(args.input_filename, "r") as file_handle:
        data = json.load(file_handle)
    # print(json.dumps(data,indent=4))

    # initialize graphviz data structure
    all_the_things = AGraph(directed=True)
    all_the_things.clear()
    all_the_things.graph_attr["label"] = "Name of graph"
    all_the_things.graph_attr["rankdir"] = "LR"

    use_cases = all_the_things.subgraph(name="cluster_use_cases", label="use cases")
    user_stories = all_the_things.subgraph(
        name="cluster_user_stories", label="user stories"
    )
    acceptance = all_the_things.subgraph(
        name="cluster_acceptance", label="acceptance tests"
    )
    regression = all_the_things.subgraph(
        name="cluster_regression", label="regression tests"
    )
    unit = all_the_things.subgraph(name="cluster_unit", label="unit tests")

    # print(data.keys())

    for this_use_case_dict in data["use cases"]:
        # print(this_use_case_dict['short name'])
        # print(this_use_case_dict)

        # the prefixes are only relevant because I have duplicate node names in JSON
        uc_prefix = "use case:"
        uc_filename_prefix="use_case_"
        use_cases.add_node(uc_prefix + this_use_case_dict["short name"],
                        URL=folder_name+"/"+uc_filename_prefix+ this_use_case_dict["short name"]+".json",
                        color="blue")
        if create_files:
            write_to_file(folder_name, this_use_case_dict, uc_filename_prefix)

        for this_user_story_dict in this_use_case_dict["user stories"]:
            # print(this_user_story_dict)
            us_prefix = "user story:"
            us_filename_prefix="user_story_"
            user_stories.add_node(us_prefix + this_user_story_dict["short name"],
                            URL=folder_name+"/"+us_filename_prefix+ this_user_story_dict["short name"]+".json",
                            color="blue")
            all_the_things.add_edge(
                uc_prefix + this_use_case_dict["short name"],
                us_prefix + this_user_story_dict["short name"],
            )
            if create_files:
                write_to_file(folder_name, this_user_story_dict, us_filename_prefix)

    for this_acceptance_dict in data["acceptance tests"]:
        acpt_prefix = "acpt:"
        acpt_filename_prefix="acpt_"
        acceptance.add_node(acpt_prefix + this_acceptance_dict["short name"],
                        URL=folder_name+"/"+acpt_filename_prefix+ this_acceptance_dict["short name"]+".json",
                        color="blue")
        if create_files:
            write_to_file(folder_name, this_acceptance_dict, acpt_filename_prefix)
    for this_regression_dict in data["regression tests"]:
        reg_prefix = "reg:"
        reg_filename_prefix = "reg_"
        regression.add_node(reg_prefix + this_regression_dict["short name"],
                        URL=folder_name+"/"+reg_filename_prefix+ this_regression_dict["short name"]+".json",
                        color="blue")
        if create_files:
            write_to_file(folder_name, this_regression_dict, reg_filename_prefix)
    for this_unit_dict in data["unit tests"]:
        unit_prefix = "unit:"
        unit_filename_prefix = "unit_"
        unit.add_node(unit_prefix + this_unit_dict["short name"],
                        URL=folder_name+"/"+unit_filename_prefix+ this_unit_dict["short name"]+".json",
                        color="blue")
        if create_files:
            write_to_file(folder_name, this_unit_dict, unit_filename_prefix)

    for edge_us_acpt in data["user-story-to-acceptance"]:
        all_the_things.add_edge(
            us_prefix + edge_us_acpt[0], acpt_prefix + edge_us_acpt[1]
        )
    for edge_acpt_reg in data["acceptance-to-regression"]:
        all_the_things.add_edge(
            acpt_prefix + edge_acpt_reg[0], reg_prefix + edge_acpt_reg[1]
        )
    for edge_reg_unit in data["regression-to-unit"]:
        all_the_things.add_edge(
            reg_prefix + edge_reg_unit[0], unit_prefix + edge_reg_unit[1]
        )

    all_the_things.write("all_the_things.dot")
    all_the_things.draw("all_the_things.svg", format="svg", prog="dot")


# this isn't a long-running program, so I'm not using logging
"""
    # maxBytes=10000 = 10kB
    # maxBytes=100000 = 100kB
    # maxBytes=1000000 = 1MB
    # maxBytes=10000000 = 10MB
    log_size = 10000000
    # maxBytes=100000000 = 100MB
    # https://gist.github.com/ibeex/3257877
    handler_debug = RotatingFileHandler(
        "critical_and_error_and_warning_and_info_and_debug.log",
        maxBytes=log_size,
        backupCount=2,
    )
    handler_debug.setLevel(logging.DEBUG)
    handler_info = RotatingFileHandler(
        "critical_and_error_and_warning_and_info.log",
        maxBytes=log_size,
        backupCount=2,
    )
    handler_info.setLevel(logging.INFO)
    handler_warning = RotatingFileHandler(
        "critical_and_error_and_warning.log",
        maxBytes=log_size,
        backupCount=2,
    )
    handler_warning.setLevel(logging.WARNING)

    # https://docs.python.org/3/howto/logging.html
    logging.basicConfig(
        # either (filename + filemode) XOR handlers
        # filename="test.log", # to save entries to file instead of displaying to stderr
        # filemode="w", # https://docs.python.org/dev/library/functions.html#filemodes
        handlers=[handler_debug, handler_info, handler_warning],
        # if the severity level is INFO,
        # the logger will handle only INFO, WARNING, ERROR, and CRITICAL messages
        # and will ignore DEBUG messages
        level=logging.DEBUG,
        format="%(asctime)s|%(filename)-13s|%(levelname)-5s|%(lineno)-4d|%(funcName)-20s|%(message)s"  # ,
        # https://stackoverflow.com/questions/6290739/python-logging-use-milliseconds-in-time-format/7517430#7517430
        # datefmt="%m/%d/%Y %I:%M:%S %f %p", # https://strftime.org/
    )

    #    logger = logging.getLogger(__name__)

    # https://docs.python.org/3/howto/logging.html
    # if the severity level is INFO, the logger will handle only INFO, WARNING, ERROR, and CRITICAL messages and will ignore DEBUG messages
    # handler.setLevel(logging.INFO)
    # handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)

    # http://matplotlib.1069221.n5.nabble.com/How-to-turn-off-matplotlib-DEBUG-msgs-td48822.html
    # https://github.com/matplotlib/matplotlib/issues/14523
    logging.getLogger("matplotlib").setLevel(logging.WARNING)


#    logger.addHandler(handler)
"""


# EOF
