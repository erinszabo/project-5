"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""


# An automated nose test suite with at least 2 test cases:
#  at least one for for DB insertion and one for retrieval.


import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)
