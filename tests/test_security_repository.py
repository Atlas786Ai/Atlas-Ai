"""SecurityRepository tests for Atlas v1.0."""

from atlas.core.exceptions import AtlasValidationError
from atlas.core.models import stable_checksum
from atlas.security.services import SecurityRepository


POLICY = {
    "policy_id": "runtime-policy",
    "role_permissions": {
        "operator": ("runtime:start", "runtime:stop"),
        "auditor": ("audit:read",),
        "admin": ("*",),
    },
    "version": "1.0.0",
}


def test_security_repository_authenticates_without_storing_raw_secret() -> None:
    repository = SecurityRepository()

    principal = repository.authenticate(
        "alice",
        roles=("operator", "auditor"),
        credential_reference="vault://alice",
        trace_id="trace-sec-001",
    )

    assert principal["principal_id"] == "alice"
    assert principal["roles"] == ("auditor", "operator")
    assert principal["authenticated"] is True
    assert principal["trace_id"] == "trace-sec-001"
    assert principal["integrity_hash"]
    assert repository._events[-1].event_type == "AuthenticationValidated"


def test_security_repository_authorizes_by_policy_and_records_decision() -> None:
    repository = SecurityRepository()
    principal = repository.authenticate("alice", roles=("operator",), credential_reference="vault://alice")

    allowed = repository.authorize(principal, "runtime:start", POLICY)
    denied = repository.authorize(principal, "audit:read", POLICY)

    assert allowed["allowed"] is True
    assert allowed["reason"] == "Allowed"
    assert denied["allowed"] is False
    assert denied["reason"] == "Denied"
    assert repository.get_security_status()["decisions"] == 2


def test_security_repository_verifies_signatures_and_archives_events() -> None:
    repository = SecurityRepository()
    payload = {"artifact": "release", "version": "1.0.0"}
    signature = stable_checksum(payload)

    assert repository.verify_signature(payload, signature) is True
    assert repository.verify_signature(payload, "bad-signature") is False

    record = repository.archive_security_event("SignatureCheck", payload, trace_id="trace-sec-002")

    assert record["payload"]["event_type"] == "SignatureCheck"
    assert record["payload"]["trace_id"] == "trace-sec-002"
    assert repository.get_security_status()["security_events"] == 1


def test_security_repository_rejects_invalid_policy_and_raw_secret() -> None:
    repository = SecurityRepository()

    try:
        repository.validate_policy({"policy_id": "bad", "role_permissions": "nope", "version": "1.0.0"})
    except AtlasValidationError:
        pass
    else:
        raise AssertionError("invalid policy was accepted")

    try:
        repository.authenticate("alice", roles=("operator",), password="plain-text")
    except AtlasValidationError as exc:
        assert exc.context["field"] == "password"
    else:
        raise AssertionError("raw secret was accepted")
