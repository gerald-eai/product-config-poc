from sqlalchemy.orm import Session
from sqlalchemy import func

# from db.models.system_mapping import SystemMappingCurrent, SystemMappingUpdates
from api.requests.system_mapping_requests import (
    CreateNewSystemMapLive,
    CreateSystemMapUpdate,
    UpdateSystemMapUpdate,
)

from schemas.system_mapping_schema import SystemMappingCurrent, SystemMappingUpdates
from typing import List


class SystemMappingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SystemMappingCurrent]:
        return (
            self.db.query(SystemMappingCurrent)
            .order_by(SystemMappingCurrent.hydraulic_system_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_hydraulic_name(self, hydraulic_name: str) -> SystemMappingCurrent:
        return (
            self.db.query(SystemMappingCurrent)
            .filter(SystemMappingCurrent.hydraulic_system_name == hydraulic_name)
            .first()
        )

    def create_new_entry(self, new_obj: CreateNewSystemMapLive) -> SystemMappingCurrent:
        sysmap_current_db = SystemMappingCurrent(**vars(new_obj))

        existing_entry = (
            self.db.query(SystemMappingCurrent)
            .filter(
                SystemMappingCurrent.hydraulic_system_name
                == sysmap_current_db.hydraulic_system_name
            )
            .all()
        )

        if len(existing_entry) > 0:
            raise ValueError(
                f"An entry already exists for Hydraulic System Name: {sysmap_current_db.hydraulic_system_name}"
            )

        self.db.add(sysmap_current_db)
        self.db.commit()
        self.db.refresh(sysmap_current_db)
        new_db_obj = self.get_by_hydraulic_name(sysmap_current_db.hydraulic_system_name)

        return new_db_obj


class SystemMappingUpdatesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SystemMappingUpdates]:
        return (
            self.db.query(SystemMappingUpdates)
            .order_by(SystemMappingUpdates.hydraulic_system_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_hydraulic_name(self, hydraulic_name: str) -> SystemMappingUpdates:
        return (
            self.db.query(SystemMappingUpdates)
            .filter(SystemMappingUpdates.hydraulic_system_name == hydraulic_name)
            .first()
        )

    def create_new_update(
        self, new_entry: CreateSystemMapUpdate
    ) -> SystemMappingUpdates:
        sys_map_db_obj = SystemMappingUpdates(**vars(new_entry))

        # check if an entry already exists
        search_db_obj = (
            self.db.query(SystemMappingUpdates)
            .filter(
                SystemMappingUpdates.hydraulic_system_name
                == sys_map_db_obj.hydraulic_system_name
            )
            .all()
        )
        if len(search_db_obj) > 0:
            raise ValueError(
                f"A pending update already exists for Hydraulic System Name: {sys_map_db_obj.hydraulic_system_name}"
            )
        self.db.add(sys_map_db_obj)
        self.db.flush()
        self.db.commit()
        self.db.refresh(sys_map_db_obj)
        new_db_obj = (
            self.db.query(SystemMappingUpdates)
            .filter(
                SystemMappingUpdates.hydraulic_system_name
                == sys_map_db_obj.hydraulic_system_name
            )
            .first()
        )
        return new_db_obj

    def updated_existing_entry(
        self, update_id: int, update_entry: UpdateSystemMapUpdate
    ) -> SystemMappingUpdates:
        sys_map_db_obj = (
            self.db.query(SystemMappingUpdates)
            .filter(SystemMappingUpdates.id == update_id)
            .first()
        )

        if sys_map_db_obj:
            for key, value in vars(update_entry).items():
                if value is not None:
                    setattr(sys_map_db_obj, key, value)
            setattr(sys_map_db_obj, "date_updated", func.now())
            self.db.commit()
            self.db.refresh(sys_map_db_obj)
            updated_db_obj = (
                self.db.query(SystemMappingUpdates)
                .filter(SystemMappingUpdates.id == update_id)
                .first()
            )
            return updated_db_obj
        else:
            return None
