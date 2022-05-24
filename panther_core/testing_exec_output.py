"""
Panther Core is a Python library for Panther Detections.
Copyright (C) 2020 Panther Labs Inc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from .detection import DetectionResult
from .policy import TYPE_POLICY, Policy
from .rule import Rule
from .exec.results import ExecutionOutput


@dataclass
class TestError:
    """Represents an error caused by any of the functions or a generic one"""

    message: Optional[str] = None


@dataclass
class FunctionTestResult:
    """Defines the result of running a function"""

    # output contains the JSON-encoded return value, None if an error was raised
    output: Optional[str]
    # error contains a TestError instance with the error message or
    # None if no error was raised
    error: Optional[TestError]
    # return value matched expectations
    matched: Optional[bool]

    @classmethod
    def new(
            cls,
            matched: bool,
            output: Optional[Union[bool, str, List[str]]],
            raw_err: Optional[str] = None,
    ) -> Optional["FunctionTestResult"]:
        """Create a new instance while applying
        the necessary transformations to the parameters"""
        if output is None and raw_err is None:
            return None

        if output is not None and not isinstance(output, str):
            output = json.dumps(output)

        return cls(output=output, error=cls.to_test_error(raw_err), matched=matched)

    @staticmethod
    def format_error(err: Optional[str], title: Optional[str] = None) -> Optional[str]:
        """Convert an error string to a structured error message"""
        if err is None:
            return None
        if title is not None:
            prefix = f"{title}: "
        else:
            prefix = ""

        return f"{prefix}{err}"

    @staticmethod
    def to_test_error(err: Optional[str], title: Optional[str] = None) -> Optional[TestError]:
        """Convert an error string to a TestError,
        also properly formatting the error message"""
        if err is None:
            return None
        return TestError(message=FunctionTestResult.format_error(err, title=title))


@dataclass  # pylint: disable=R0902
class TestResultsPerFunction:
    """Container for the results of each function"""

    detectionFunction: Optional[FunctionTestResult]  # pylint: disable=C0103
    titleFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103
    dedupFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103
    alertContextFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103
    descriptionFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103
    referenceFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103
    severityFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103
    runbookFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103
    destinationsFunction: Optional[FunctionTestResult] = None  # pylint: disable=C0103


@dataclass  # pylint: disable=R0902
class TestResult:
    """The structure of the results for a test case evaluation"""

    id: Optional[str]  # pylint: disable=C0103
    name: str
    # The following two fields do not conform to Python's naming
    # conventions, but the field names correspond
    # to response attributes by API & FE.
    # TODO: provide a field name translation step if necessary
    detectionId: Optional[str]  # pylint: disable=C0103
    genericError: Optional[str]  # pylint: disable=C0103
    error: Optional[TestError]
    errored: bool
    passed: bool
    trigger_alert: Optional[bool]
    functions: TestResultsPerFunction


@dataclass
class TestExpectations:
    """Contains the expected values for performing assertions"""

    detection: bool
    # TODO: include assertions for remaining functions, e.g title and alert context


@dataclass
class TestSpecification:
    """The structure of a test case"""

    id: str  # pylint: disable=C0103
    name: str
    data: Dict[str, Any]
    mocks: List[Dict[str, Any]]
    expectations: TestExpectations


# pylint: disable=too-few-public-methods
class TestCaseEvaluator:
    """Translates detection execution results to test case results,
    by performing assertions and determining the status"""

    def __init__(self, spec: TestSpecification, exec_output: ExecutionOutput):
        self._spec = spec
        self._exec_output = exec_output
        self._exec_match = exec_output.match

    def _get_result_status(self) -> bool:
        """Get the test status - passing/failing"""
        # Aux functions are executed unconditionally
        # (regardless if the detection matched or not) during testing.
        # Only if the detection is expected to trigger an alert,
        # we want to include errors from other functions in the status.
        if self._spec.expectations.detection == self._get_detection_alert_value():
            return self._exec_output.trigger_alert and not self._exec_output.errored
        # expectations match the detection output
        return self._spec.expectations.detection == self._exec_output.details.primary_functions.detection.output

    def _get_generic_error_details(self) -> Tuple[Optional[str], Optional[str]]:
        generic_error = None
        generic_error_title = None
        if self._exec_output.details.input_error is not None:
            generic_error = self._exec_output.details.input_error
            generic_error_title = "Invalid event"
        elif self._exec_output.details.setup_error is not None:
            generic_error = self._exec_output.details.setup_error
        return generic_error, generic_error_title

    def _get_detection_alert_value(self) -> bool:
        if self._exec_match and self._exec_match.detectionType.upper() == TYPE_POLICY.upper():
            return Policy.matcher_alert_value
        return Rule.matcher_alert_value

    def interpret(self, ignore_exception_types: List[Type[Exception]] = None) -> TestResult:
        """Evaluate the detection result taking into account
        the errors raised during evaluation and
        the test specification expectations"""

        # first, we should update the detection result, taking into account any
        # ignored exception types passed into this test

        function_results = dict(
            detectionFunction=FunctionTestResult.new(
                self._spec.expectations.detection == self._exec_output.details.primary_functions.detection.output,
                self._exec_output.details.primary_functions.detection.output,
                ignoreable_exception(self._exec_output.details.primary_functions.detection.error,
                                     ignore_exception_types),
            )
        )

        # We don't include output from other functions
        # unless the test was expected to match and trigger an alert.
        # If the test fails, providing all the output provides a faster feedback loop,
        # on possible additional failures.
        if self._spec.expectations.detection == self._get_detection_alert_value():
            function_results.update(
                dict(
                    titleFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.title.error is None,
                        self._exec_output.details.aux_functions.title.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.title.error,
                                             ignore_exception_types),
                    ),
                    descriptionFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.description.error is None,
                        self._exec_output.details.aux_functions.description.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.description.error,
                                             ignore_exception_types),
                    ),
                    referenceFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.reference.error is None,
                        self._exec_output.details.aux_functions.reference.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.reference.error,
                                             ignore_exception_types),
                    ),
                    severityFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.severity.error is None,
                        self._exec_output.details.aux_functions.severity.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.severity.error,
                                             ignore_exception_types),
                    ),
                    runbookFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.runbook.error is None,
                        self._exec_output.details.aux_functions.runbook.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.runbook.error,
                                             ignore_exception_types),
                    ),
                    destinationsFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.destinations.error is None,
                        self._exec_output.details.aux_functions.destinations.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.destinations.error,
                                             ignore_exception_types),
                    ),
                    dedupFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.dedup.error is None,
                        self._exec_output.details.aux_functions.dedup.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.dedup.error,
                                             ignore_exception_types),
                    ),
                    alertContextFunction=FunctionTestResult.new(
                        self._exec_output.details.aux_functions.alert_context.error is None,
                        self._exec_output.details.aux_functions.alert_context.output,
                        ignoreable_exception(self._exec_output.details.aux_functions.alert_context.error,
                                             ignore_exception_types),
                    ),
                )
            )

        generic_error, generic_error_title = self._get_generic_error_details()

        return TestResult(
            id=self._spec.id,
            name=self._spec.name,
            detectionId=self._exec_match.detectionId if self._exec_match else '',
            genericError=FunctionTestResult.format_error(
                generic_error, title=generic_error_title
            ),
            errored=self._exec_output.errored,
            error=FunctionTestResult.to_test_error(generic_error, title=generic_error_title),
            # Passing or failing test?
            passed=self._get_result_status(),
            trigger_alert=self._exec_output.trigger_alert,
            functions=TestResultsPerFunction(**function_results),
        )


def ignoreable_exception(exception: Any,
                         ignore_exception_types: List[Type[Exception]] = None) -> Optional[str]:
    if ignore_exception_types:
        for exception_type in ignore_exception_types:
            if repr(exception_type) == exception:
                return None
    return exception
