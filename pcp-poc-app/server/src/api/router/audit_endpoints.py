from fastapi import APIRouter, Depends
from api.dependencies import get_audit_log_service
from services.audit_log_service import AuditLogService
from schemas.audit_log_schema import AuditLog
from typing import List


router = APIRouter(prefix="/audit", tags=["Audit Log APIs"])


@router.get("/", response_model=List[AuditLog])
def get_all(
    skip: int = 0,
    limit: int = 100,
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    """Returns a paginated list of records in the Audit log.

    Args:
        skip (int, optional): The page offset. Defaults to 0.
        limit (int, optional): Max no. of records to return per page. Defaults to 100.
        audit_service (AuditLogService, optional): Audit log dependency service. Defaults to Depends(get_audit_log_service).

    Returns:
        List[AuditLog]: Paginated list of audit log records.
    """
    audit_response = audit_service.get_all(skip, limit)
    return audit_response


@router.get("/{event_id}", response_model=AuditLog)
def get_by_event_id(
    event_id: str, audit_service: AuditLogService = Depends(get_audit_log_service)
):
    """Returns an Audit log record that matches the event id provided.

    Args:
        event_id (str): id being queried
        audit_service (AuditLogService, optional): Audit log dependency service. Defaults to Depends(get_audit_log_service).

    Returns:
        AuditLog: Audit log record that matches the id.
    """
    audit_response = audit_service.get_by_event_id(event_id)
    return audit_response
