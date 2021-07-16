import json
import os.path
import typing
import unittest
from typing import List
from app import _clear_page


class TestCaseData(typing.TypedDict):
    item: str
    expect: List[str]
    ind: int


class TestClearPage(unittest.TestCase):
    cases: List[TestCaseData]

    def setUp(self) -> None:
        with open(os.path.join("test", "cases.json")) as case_file:
            self.cases = json.load(case_file)

    def _execute_case(self, case: TestCaseData):
        assert _clear_page(case['ind'], case['item']) == case['expect']

    def test_clear_page(self):
        for case in self.cases:
            self._execute_case(case)
