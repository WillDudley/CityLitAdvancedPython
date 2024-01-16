"""
This file...

Created...
"""


class Employee:

    def __init__(self, name: str, dept: str, job: str, wage: str, manager: str, address: str):
        self.name = name
        self.dept = dept
        self.job = job
        self.wage = wage
        self.manager = manager
        self.address = address

        self.yearsAtCompany = 0

