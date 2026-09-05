from backend.app.core.audit import AuditLogger


def test_audit_logger_records_events():
    logger = AuditLogger()

    logger.log(
        stage="document_agent",
        status="completed",
    )

    events = logger.all()

    assert len(events) == 1
    assert events[0]["stage"] == "document_agent"
    assert events[0]["status"] == "completed"
    assert events[0]["timestamp"]