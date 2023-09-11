from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
from core.config import app_env


class SresCurrent(SQLModel, table=True):
    __tablename__ = "pcp_poc_sres"
    __table_args__ = (
        {"schema": "DPSN_DEMO"} if app_env == "local" else {"schema": "DPSN"}
    )

    odmt_sres_id: int = Field(primary_key=True, index=True)
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str

    # optional params
    operating_level: Optional[float]
    bwl: Optional[float]
    twl: Optional[float]
    capacity: Optional[float]
    include_exclude: Optional[str]
    comments: Optional[str]
    include_in_dv: Optional[int]
    turnover_target_lower: Optional[float]
    turnover_target_upper: Optional[float]
    sm_record_id: Optional[str]
    validated_tag: Optional[str]
    last_modified: Optional[datetime]
    production_state: Optional[str]

    def __repr__(self):
        return f"SRES ID: {self.odmt_sres_id} \
            Hydraulic System Name: {self.hydraulic_system_name} \
            SRES Name: {self.sres_name} \
            Cell Name: {self.cell_name} \
            PI Tag Name: {self.pi_tag_name} \
            Engineering Unit: {self.engineering_unit}"
