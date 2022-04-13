#!/usr/bin/env python3

# Ben Payne, 2021
# https://creativecommons.org/licenses/by/4.0/
# Attribution 4.0 International (CC BY 4.0)

"""
"""

import os
import json

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


if __name__ == "__main__":

    # TODO: make this a user argument
    create_files=True

    folder_name="output"
    if create_files:
        os.mkdir(folder_name)

    # TODO: replace hardcoded filename with user defined filename as argument
    with open("use_cases_and_user_stories_and_acceptance_tests.json","r") as file_handle:
        data = json.load(file_handle)
    #print(json.dumps(data,indent=4))

    all_the_things = AGraph(directed=True)
    all_the_things.clear()
    all_the_things.graph_attr["label"] = "Name of graph"
    all_the_things.graph_attr["rankdir"] = "LR"


    use_cases = all_the_things.subgraph(name="cluster_use_cases",label="use cases")
    user_stories = all_the_things.subgraph(name="cluster_user_stories",label="user stories")
    acceptance = all_the_things.subgraph(name="cluster_acceptance",label="acceptance tests")
    regression = all_the_things.subgraph(name="cluster_regression",label="regression tests")
    unit = all_the_things.subgraph(name="cluster_unit",label="unit tests")

    #print(data.keys())

    for this_use_case_dict in data['use cases']:
        #print(this_use_case_dict['short name'])
        #print(this_use_case_dict)

        # the prefixes are only relevant because I have duplicate node names in JSON
        uc_prefix = "use case:"
        use_cases.add_node(uc_prefix+this_use_case_dict['short name'])
        if create_files:
            with open(folder_name+"/use_case_"+this_use_case_dict['short name']+".json","w") as file_handle:
                json.dump(this_use_case_dict,file_handle,indent=2)
        for this_user_story_dict in this_use_case_dict['user stories']:
            #print(this_user_story_dict)
            us_prefix = "user story:"
            user_stories.add_node(us_prefix+this_user_story_dict['short name'])
            all_the_things.add_edge(uc_prefix+this_use_case_dict['short name'],us_prefix+this_user_story_dict['short name'])
            if create_files:
                with open(folder_name+"/user_story_"+this_user_story_dict['short name']+".json","w") as file_handle:
                    json.dump(this_user_story_dict,file_handle,indent=2)

    for this_acceptance_dict in data['acceptance tests']:
        acpt_prefix = "acpt:"
        acceptance.add_node(acpt_prefix+this_acceptance_dict['short name'])
        if create_files:
            with open(folder_name+"/acpt_"+this_acceptance_dict['short name']+".json","w") as file_handle:
                json.dump(this_acceptance_dict,file_handle,indent=2)
    for this_regression_dict in data['regression tests']:
        reg_prefix = "reg:"
        regression.add_node(reg_prefix+this_regression_dict['short name'])
        if create_files:
            with open(folder_name+"/reg_"+this_regression_dict['short name']+".json","w") as file_handle:
                json.dump(this_regression_dict,file_handle,indent=2)
    for this_unit_dict in data['unit tests']:
        unit_prefix = "unit:"
        unit.add_node(unit_prefix+this_unit_dict['short name'])
        if create_files:
            with open(folder_name+"/unit_"+this_unit_dict['short name']+".json","w") as file_handle:
                json.dump(this_unit_dict,file_handle,indent=2)

    for edge_us_acpt in data['user-story-to-acceptance']:
        all_the_things.add_edge(us_prefix+edge_us_acpt[0],acpt_prefix+edge_us_acpt[1])
    for edge_acpt_reg in data['acceptance-to-regression']:
        all_the_things.add_edge(acpt_prefix+edge_acpt_reg[0],reg_prefix+edge_acpt_reg[1])
    for edge_reg_unit in data['regression-to-unit']:
        all_the_things.add_edge(reg_prefix+edge_reg_unit[0],unit_prefix+edge_reg_unit[1])

    all_the_things.write("all_the_things.dot")
    all_the_things.draw("all_the_things.svg", format="svg", prog="dot")


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
