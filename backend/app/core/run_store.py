from typing import Any


class RunStore:
    def __init__(self):
        self._runs: dict[str, dict[str, Any]] = {}
        self._counter = 0

    def create(self, state: dict[str, Any]) -> str:
        self._counter += 1
        run_id = f"INDRA-{self._counter:04d}"

        self._runs[run_id] = state

        return run_id

    def get(self, run_id: str) -> dict[str, Any]:
        if run_id not in self._runs:
            raise KeyError(f"Run not found: {run_id}")

        return self._runs[run_id]

    def update(
        self,
        run_id: str,
        updates: dict[str, Any],
    ) -> dict[str, Any]:
        run = self.get(run_id)
        run.update(updates)
        return run

    def all(self) -> dict[str, dict[str, Any]]:
        return dict(self._runs)