"""
Panther Analysis Tool is a command line interface for writing,
testing, and packaging policies/rules.
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


import unittest

from panther_core.detection import DetectionResult
from panther_core.policy import TYPE_POLICY
from panther_core.rule import Rule, TYPE_RULE, ERROR_TYPE_RULE
from panther_core.exec.results import ExecutionOutput, ExecutionMatch, ExecutionDetails, \
    ExecutionDetailsPrimaryFunctions, ExecutionPrimaryFunctionDetails, ExecutionDetailsAuxFunctions, \
    ExecutionAuxFunctionDetails

from panther_core.testing import FunctionTestResult, TestError, TestSpecification, \
    TestExpectations, TestCaseEvaluator, TestResult, TestResultsPerFunction, TestCaseEvaluatorExec

TEST_RULE = {
    'body': 'def rule(_):\n\treturn True',
    'id': 'test-id',
    'severity': 'INFO',
    'type': TYPE_RULE,
    'versionId': 'my-version',
}

class TestTestCaseEvaluator2(unittest.TestCase):

    def test_interpret_passing_test_not_expected_to_trigger_alert(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=False))
        exec_match = None
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    output=False
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(defined=False),
                runbook=ExecutionAuxFunctionDetails(defined=False),
                severity=ExecutionAuxFunctionDetails(defined=False),
                reference=ExecutionAuxFunctionDetails(defined=False),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(defined=False),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            )
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='',
            genericError=None,
            error=None,
            errored=False,
            passed=True,
            trigger_alert=False,
            functions=TestResultsPerFunction(
                detectionFunction=FunctionTestResult(output='false', error=None, matched=True),
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

    def test_interpret_passing_test_expected_to_trigger_alert(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=True))
        exec_match = ExecutionMatch(
            severity='INFO',
            detectionId=spec.id,
            detectionType=TYPE_RULE,
            alertType=TYPE_RULE,
            detectionTags=None,
            detectionVersion='',
            detectionReports=None,
            dedupString='',
            detectionSeverity='INFO',
            dedupPeriodMins='',
            event=None
        )
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    output=True
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(defined=False),
                runbook=ExecutionAuxFunctionDetails(defined=False),
                severity=ExecutionAuxFunctionDetails(defined=False),
                reference=ExecutionAuxFunctionDetails(defined=False),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(defined=False),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            )
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='test-id',
            genericError=None,
            error=None,
            errored=False,
            passed=True,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=FunctionTestResult(output='true', error=None, matched=True),
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

    def test_interpret_failing_test_expected_to_trigger_alert(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=True))
        exec_match = ExecutionMatch(
            severity='INFO',
            detectionId=spec.id,
            detectionType=TYPE_RULE,
            alertType=ERROR_TYPE_RULE,
            detectionTags=None,
            detectionVersion='',
            detectionReports=None,
            dedupString='',
            detectionSeverity='INFO',
            dedupPeriodMins='',
            event=None
        )
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    error=TypeError('wrong type'),
                    output=None
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(defined=False),
                runbook=ExecutionAuxFunctionDetails(defined=False),
                severity=ExecutionAuxFunctionDetails(defined=False),
                reference=ExecutionAuxFunctionDetails(defined=False),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(defined=False),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            )
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='test-id',
            genericError=None,
            error=None,
            errored=True,
            passed=False,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=FunctionTestResult(output=None, error=TestError(message='TypeError: wrong type'), matched=False),
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)
    
    def test_interpret_failing_test_expected_to_match_aux_function_error(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=True))
        exec_match = ExecutionMatch(
            severity='INFO',
            detectionId=spec.id,
            detectionType=TYPE_RULE,
            alertType=TYPE_RULE,
            detectionTags=None,
            detectionVersion='',
            detectionReports=None,
            dedupString='',
            detectionSeverity='INFO',
            dedupPeriodMins='',
            event=None
        )
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    output=True
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(
                    defined=True,
                    error=TypeError('wrong type')
                ),
                runbook=ExecutionAuxFunctionDetails(defined=False),
                severity=ExecutionAuxFunctionDetails(defined=False),
                reference=ExecutionAuxFunctionDetails(defined=False),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(defined=False),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            )
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='test-id',
            genericError=None,
            error=None,
            errored=True,
            passed=False,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=FunctionTestResult(output='true', error=None, matched=True),
                titleFunction=FunctionTestResult(output=None, error=TestError(message='TypeError: wrong type'), matched=False),
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

    def test_interpret_failing_test_expected_to_trigger_alert_detection_error(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=False))
        exec_match = ExecutionMatch(
            severity='INFO',
            detectionId=spec.id,
            detectionType=TYPE_RULE,
            alertType=TYPE_RULE,
            detectionTags=None,
            detectionVersion='',
            detectionReports=None,
            dedupString='',
            detectionSeverity='INFO',
            dedupPeriodMins='',
            event=None
        )
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    error=TypeError('wrong type'),
                    output=None,
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(defined=False),
                runbook=ExecutionAuxFunctionDetails(defined=False),
                severity=ExecutionAuxFunctionDetails(defined=False),
                reference=ExecutionAuxFunctionDetails(defined=False),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(defined=False),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            )
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='test-id',
            genericError=None,
            error=None,
            errored=True,
            passed=False,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=FunctionTestResult(output=None, error=TestError(message='TypeError: wrong type'), matched=False),
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

    def test_interpret_failing_test_expected_to_trigger_alert_with_aux_exception(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=False))
        exec_match = ExecutionMatch(
            severity='INFO',
            detectionId=spec.id,
            detectionType=TYPE_RULE,
            alertType=TYPE_RULE,
            detectionTags=None,
            detectionVersion='',
            detectionReports=None,
            dedupString='',
            detectionSeverity='INFO',
            dedupPeriodMins='',
            event=None
        )
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    output=False,
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(
                    defined=False,
                    error=TypeError('wrong type')
                ),
                runbook=ExecutionAuxFunctionDetails(
                    defined=True,
                    error=TypeError('wrong type')

                ),
                severity=ExecutionAuxFunctionDetails(
                    defined=False,
                    error=TypeError('wrong type')
                ),
                reference=ExecutionAuxFunctionDetails(
                    defined=True,
                    error=TypeError('wrong type')
                ),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(
                    defined=True,
                    error=TypeError('wrong type')
                ),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            )
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='test-id',
            genericError=None,
            error=None,
            errored=True,
            passed=True,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=FunctionTestResult(output='false', error=None, matched=True),
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None,
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

    def test_interpret_failing_test_policy_expected_to_trigger_alert_with_aux_exception(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=True))
        exec_match = ExecutionMatch(
            severity='INFO',
            detectionId=spec.id,
            detectionType=TYPE_POLICY,
            alertType=TYPE_POLICY,
            detectionTags=None,
            detectionVersion='',
            detectionReports=None,
            dedupString='',
            detectionSeverity='INFO',
            dedupPeriodMins='',
            event=None
        )
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    output=True,
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(
                    defined=False,
                    error=TypeError('wrong type')
                ),
                runbook=ExecutionAuxFunctionDetails(
                    defined=True,
                    error=TypeError('wrong type')

                ),
                severity=ExecutionAuxFunctionDetails(
                    defined=False,
                    error=TypeError('wrong type')
                ),
                reference=ExecutionAuxFunctionDetails(
                    defined=True,
                    error=TypeError('wrong type')
                ),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(
                    defined=True,
                    error=TypeError('wrong type')
                ),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            )
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='test-id',
            genericError=None,
            error=None,
            errored=True,
            passed=True,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=FunctionTestResult(output='true', error=None, matched=True),
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None,
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

    def test_interpret_failing_test_input_error(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=False))
        exec_match = None
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    output=None,
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(defined=False),
                runbook=ExecutionAuxFunctionDetails(defined=False),
                severity=ExecutionAuxFunctionDetails(defined=False),
                reference=ExecutionAuxFunctionDetails(defined=False),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(defined=False),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            ),
            input_error=TypeError('wrong type')
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='',
            genericError='Invalid event: TypeError: wrong type',
            error=TestError(message='Invalid event: TypeError: wrong type'),
            errored=True,
            passed=False,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=None,
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

    def test_interpret_generic_error(self) -> None:
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=False))
        exec_match = None
        exec_details = ExecutionDetails(
            primary_functions=ExecutionDetailsPrimaryFunctions(
                detection=ExecutionPrimaryFunctionDetails(
                    output=None,
                )
            ),
            aux_functions=ExecutionDetailsAuxFunctions(
                title=ExecutionAuxFunctionDetails(defined=False),
                runbook=ExecutionAuxFunctionDetails(defined=False),
                severity=ExecutionAuxFunctionDetails(defined=False),
                reference=ExecutionAuxFunctionDetails(defined=False),
                description=ExecutionAuxFunctionDetails(defined=False),
                destinations=ExecutionAuxFunctionDetails(defined=False),
                dedup=ExecutionAuxFunctionDetails(defined=False),
                alert_context=ExecutionAuxFunctionDetails(defined=False)
            ),
            setup_error=TypeError('wrong type')
        )
        exec_output = ExecutionOutput(
            input_id=spec.id,
            match=exec_match,
            details=exec_details
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='',
            genericError='TypeError: wrong type',
            error=TestError(message='TypeError: wrong type'),
            errored=True,
            passed=False,
            trigger_alert=True,
            functions=TestResultsPerFunction(
                detectionFunction=None,
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluatorExec(spec=spec, exec_output=exec_output).interpret()
        self.assertEqual(expected, actual)

        # Event compatibility exception
        spec = TestSpecification(id='test-id', name='test-name', data={}, mocks=[], expectations=TestExpectations(detection=False))
        detection_result = DetectionResult(
            detection_id=spec.id,
            trigger_alert=False,
            input_exception=TypeError('wrong type'),
            detection_severity='INFO',
            detection_type=TYPE_RULE
        )
        expected = TestResult(
            id='test-id',
            name='test-name',
            detectionId='test-id',
            genericError='Invalid event: TypeError: wrong type',
            error=TestError(message='Invalid event: TypeError: wrong type'),
            errored=True,
            passed=False,
            trigger_alert=False,
            functions=TestResultsPerFunction(
                detectionFunction=None,
                titleFunction=None,
                dedupFunction=None,
                alertContextFunction=None,
                descriptionFunction=None,
                referenceFunction=None,
                severityFunction=None,
                runbookFunction=None,
                destinationsFunction=None
            )
        )
        actual = TestCaseEvaluator(spec=spec, detection_result=detection_result).interpret()
        self.assertEqual(expected, actual)
