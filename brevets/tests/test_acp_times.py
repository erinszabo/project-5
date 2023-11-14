"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

# test if the last distance is less than the total distance, 
# an exception is thrown
#     ex: the last control point (120.00 km) must be at least 200 km

# test if the last distance is MORE than 20% of the total distance, 
# an exception is thrown
#     ex: the last control point (250.00 km) is over 20% longer than 
#         the theoretical distance (200 km): error in selecting units?

# test if the last distance less than OR equal to 20% more than the total distance, 
# no exception is thown, and calculation is based on total distance and not last distance


# An automated nose test suite with at least 2 test cases:
#  at least one for for DB insertion and one for retrieval.


import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)
