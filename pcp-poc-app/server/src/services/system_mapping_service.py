# from db.models.system_mapping import SystemMappingCurrent, SystemMappingUpdates
from sqlalchemy.orm import Session
from db.sytem_mapping_repository import (
    SystemMappingRepository,
    SystemMappingUpdatesRepository,
)
from schemas.system_mapping_schema import SystemMappingCurrent, SystemMappingUpdate
from api.requests.system_mapping_requests import (
    CreateSystemMapUpdate,
    UpdateSystemMapUpdate,
)


class SystemMappingService:
    def __init__(self, db: Session):
        self.repository = SystemMappingRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.repository.get_all(skip, limit)
        return [SystemMappingCurrent.from_db(el) for el in query]

    def get_by_hydraulic_name(self, hydraulic_name: str):
        query = self.repository.get_by_hydraulic_name(hydraulic_name)
        return SystemMappingCurrent.from_db(query)


class SystemMappingUpdateService:
    def __init__(self, db: Session):
        self.repository = SystemMappingUpdatesRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        query = self.repository.get_all(skip, limit)
        return [SystemMappingUpdate.from_db(el) for el in query]

    def get_by_hydraulic_name(self, hydraulic_name: str):
        query = self.repository.get_by_hydraulic_name(hydraulic_name)
        return SystemMappingUpdate.from_db(query)

    def create_new_update(self, new_sys_map: CreateSystemMapUpdate):
        new_sys_map_obj = self.repository.create_new_update(new_entry=new_sys_map)
        return SystemMappingUpdate.from_db(new_sys_map_obj)

    def update_existing_entry(
        self, update_id: int, modified_sys_map: UpdateSystemMapUpdate
    ):
        modified_sys_map_obj = self.repository.updated_existing_entry(
            update_id, modified_sys_map
        )
        return SystemMappingUpdate.from_db(modified_sys_map_obj)
