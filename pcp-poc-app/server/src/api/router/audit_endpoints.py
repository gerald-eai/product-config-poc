from fastapi import APIRouter, Depends
from api.dependencies import get_audit_log_service
from services.audit_log_service import AuditLogService
from schemas.audit_log_schema import AuditLogBase


router = APIRouter(prefix="/audit", tags=["Audit Log APIs"])


@router.get("/", response_model=list[AuditLogBase])
def get_all(
    skip: int = 0,
    limit: int = 100,
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    audit_response = audit_service.get_all(skip, limit)
    print(audit_response)
    return audit_response

@router.get("/{event_id}", response_model=AuditLogBase)
def get_by_event_id(event_id: str, audit_service: AuditLogService=Depends(get_audit_log_service)): 
    audit_response = audit_service.get_by_event_id(event_id)
    return audit_response 
