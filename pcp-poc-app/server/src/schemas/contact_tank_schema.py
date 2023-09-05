from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel


class ContactTankCurrent(SQLModel, table=True):
    __tablename__ = "pcp_poc_contact_tanks"
    __table_args__ = {"schema": "DPSN"}

    odmt_contact_tank_id: int = Field(primary_key=True, index=True)
    hydraulic_system_name: Optional[str] = Field(
        foreign_key="DPSN.pcp_poc_system_mapping.hydraulic_system_name"
    )
    sres_name: str = Field(index=True)
    cell_name: str = Field(index=True)
    pi_tag_name: str = Field(index=True)
    engineering_unit: Optional[str] = Field(index=True)
    validated_tag: Optional[str] = Field(default=None)
    operating_level: Optional[float] = Field(default=None)
    bwl: Optional[float] = Field(default=None)
    twl: Optional[float] = Field(default=None)
    capacity: Optional[float] = Field(default=None)
    comments: Optional[str] = Field(default=None)
    include_SDSR: Optional[int] = Field(default=None)
    include_SRV: Optional[int] = Field(default=None)
    include_WPRO: Optional[int] = Field(default=None)
    cell_status: Optional[str]

    last_modified: Optional[datetime] = Field(
        default=datetime.now(), sa_column=Column(DateTime(timezone=True))
    )

#     def __repr__(self):
#         values = ', '.join([f"{column.name}='{getattr(self, column.name)}'" for column in self.__table__.columns])
#         return f"{self.__class__.__name__}({values})"


class ContactTankUpdates(SQLModel, table=True):
    __tablename__ = "pcp_poc_contact_tanks_updates"
    __table_args__ = {"schema": "DPSN"}

    id: int = Field(primary_key=True, index=True)
    odmt_contact_tank_id: int = Field(
        index=True, foreign_key="DPSN.pcp_poc_contact_tanks.odmt_contact_tank_id"
    )
    hydraulic_system_name: Optional[str] = Field(
        foreign_key="DPSN.pcp_poc_system_mapping.hydraulic_system_name"
    )
    sres_name: Optional[str] = Field(index=True, default=None)
    cell_name: Optional[str] = Field(index=True, default=None)
    pi_tag_name: Optional[str] = Field(index=True, default=None)
    engineering_unit: Optional[str] = Field(default=None)
    validated_tag: Optional[str] = Field(default=None)
    operating_level: Optional[float] = Field(default=None)
    bwl: Optional[float] = Field(default=None)
    twl: Optional[float] = Field(default=None)
    capacity: Optional[float] = Field(default=None)
    comments: Optional[str] = Field(default=None)
    include_SDSR: Optional[int] = Field(default=None)
    include_SRV: Optional[int] = Field(default=None)
    include_WPRO: Optional[int] = Field(default=None)
    cell_status: Optional[str]

    date_updated: Optional[datetime] = Field(
        default=datetime.now(), sa_column=Column(DateTime(timezone=True))
    )
    
#     def __repr__(self):
#         values = ', '.join([f"{column.name}='{getattr(self, column.name)}'" for column in self.__table__.columns])
#         return f"{self.__class__.__name__}({values})"

