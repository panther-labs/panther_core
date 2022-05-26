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
import unittest

from panther_core.exec.common import ExecutionMode, ExecutionMatch

from panther_core.exec.task import (
    ExecutionEnv,
    ExecutionTask,
    ExecutionTaskEnv,
    ExecutionTaskInput,
    ExecutionTaskOutput,
    ExecutionTaskOptions,
)

from panther_core.exec.results import (
    ExecutionOutput,
    ExecutionResult,
    ExecutionDetails,
    ExecutionAuxFunctionDetails,
    ExecutionPrimaryFunctionDetails,
    ExecutionDetailsAuxFunctions,
    ExecutionDetailsPrimaryFunctions,
)


class TestSerialization(unittest.TestCase):

    def test_mode(self) -> None:
        obj = ExecutionMode.INLINE

        self.assertEqual('"INLINE"', json.dumps(obj))

    def test_task_input(self) -> None:
        obj = ExecutionTaskInput(
            mode=ExecutionMode.INLINE,
            data=[dict(xyz=1), dict(xyz=2)],
            input_id_field="xyz",
        )

        self.assertEqual(
            obj.to_json(),
            json.dumps(
                dict(
                    mode="INLINE",
                    data=[dict(xyz=1), dict(xyz=2)],
                    input_id_field="xyz",
                    url=None,
                )
            )
        )

    def test_task(self) -> None:
        obj_a = ExecutionTask(
            env=ExecutionTaskEnv(
                mode=ExecutionMode.INLINE,
                url=None,
                env=ExecutionEnv(
                    mocks=[dict(id="a")],
                    outputs=[dict(id="b")],
                    globals=[dict(id="a")],
                    detections=[dict(id="b")],
                    data_models=[],
                )
            ),
            input=ExecutionTaskInput(
                url=None,
                mode=ExecutionMode.INLINE,
                data=[],
                input_id_field="some_field",
            ),
            output=ExecutionTaskOutput(
                url=None,
                mode=ExecutionMode.INLINE,
            ),
            options=ExecutionTaskOptions(
                execution_details=False,
            ),
        )

        self.assertNotEqual("", obj_a.to_json())
        self.assertEqual(obj_a, ExecutionTask.from_json(json.loads(obj_a.to_json())))

    def test_result(self) -> None:
        obj_a = ExecutionResult(
            url="https://en.wikipedia.org",
            output_mode=ExecutionMode.INLINE,
            data=[
                ExecutionOutput(
                    input_id="xyz",
                    match=ExecutionMatch(
                        detectionId="1",
                        alertType="RULE",
                        detectionType="RULE",
                        detectionVersion="0",
                        detectionTags=[],
                        detectionReports={},
                        detectionSeverity="INFO",
                        dedupString="",
                        dedupPeriodMins=0,
                        event={}
                    ),
                    details=ExecutionDetails(
                        aux_functions=ExecutionDetailsAuxFunctions(
                            dedup=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                            title=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                            runbook=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                            severity=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                            reference=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                            description=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                            destinations=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                            alert_context=ExecutionAuxFunctionDetails(
                                defined=True,
                                error=None,
                                output="boop",
                            ),
                        ),
                        primary_functions=ExecutionDetailsPrimaryFunctions(
                            detection=ExecutionPrimaryFunctionDetails(
                                error=None,
                                output=False,
                            ),
                        )
                    )
                )
            ]
        )

        obj_b = ExecutionResult.from_json(json.loads(obj_a.to_json()))
        self.assertEqual(obj_a, obj_b)
