import json
import unittest

from ..common import ExecutionMode

from ..task import (
    ExecutionTaskInput,
)

from ..results import (
    ExecutionResult,
    ExecutionDetails,
    ExecutionDetailsAuxFunctions,
    ExecutionAuxFunctionDetails
)


class TestSerialization(unittest.TestCase):

    def test_mode(self) -> None:
        obj = ExecutionMode.INLINE

        self.assertEqual('"INLINE"', json.dumps(obj))

    def test_task_input(self) -> None:
        obj = ExecutionTaskInput(
            url=None,
            mode=ExecutionMode.INLINE,
            rows=[dict(xyz=1), dict(xyz=2)],
            input_id_field="xyz",
        )

        self.assertEqual(
            obj.to_json(),
            json.dumps(
                dict(
                    mode="INLINE",
                    url=None,
                    rows=[dict(xyz=1), dict(xyz=2)],
                    input_id_field="xyz",
                )
            )
        )

    def test_result(self) -> None:
        obj_a = ExecutionResult(
            url="https://en.wikipedia.org",
            output_mode=ExecutionMode.INLINE,
            data=[
                dict(p_row_id="1"),
            ],
            details=[
                ExecutionDetails(
                    input_id="xyz",
                    aux_functions=ExecutionDetailsAuxFunctions(
                        title=ExecutionAuxFunctionDetails(
                            error=None,
                            output="boop",
                        ),
                        runbook=ExecutionAuxFunctionDetails(
                            error=None,
                            output="boop",
                        ),
                        severity=ExecutionAuxFunctionDetails(
                            error=None,
                            output="boop",
                        ),
                        reference=ExecutionAuxFunctionDetails(
                            error=None,
                            output="boop",
                        ),
                        description=ExecutionAuxFunctionDetails(
                            error=None,
                            output="boop",
                        ),
                        destinations=ExecutionAuxFunctionDetails(
                            error=None,
                            output="boop",
                        ),
                        alert_context=ExecutionAuxFunctionDetails(
                            error=None,
                            output="boop",
                        ),
                    )
                )
            ]
        )

        obj_b = ExecutionResult.from_json(json.loads(obj_a.to_json()))

        self.assertEqual(obj_a, obj_b)
