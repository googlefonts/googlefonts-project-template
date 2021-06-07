#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Result(object):
    """
    Data object that maintains test result success status and test result message
    (intended for std output to user)
    """

    def __init__(self, filepath):
        self.test_filepath = filepath
        # test result indicator, True = test failed, False = test succeeded
        self.test_failed = None
        # when set to True, sys.exit(1) raised immediately on this error result
        self.exit_failure = None
        # maintains std output string to be presented to user for each test result
        self.test_long_stdstream_string = ""
