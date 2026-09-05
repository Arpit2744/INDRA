from backend.app.core.run_store import RunStore


def test_run_store_creates_and_retrieves_run():
    store = RunStore()

    run_id = store.create(
        {
            "status": "pending",
            "request": "Investigate C-101.",
        }
    )

    assert run_id == "INDRA-0001"

    run = store.get(run_id)

    assert run["status"] == "pending"
    assert run["request"] == "Investigate C-101."


def test_run_store_updates_run():
    store = RunStore()

    run_id = store.create(
        {
            "status": "pending",
        }
    )

    updated = store.update(
        run_id,
        {
            "status": "approved",
        },
    )

    assert updated["status"] == "approved"