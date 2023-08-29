from sqlalchemy.orm import Session
from db.sytem_mapping_repository import (
    SystemMappingRepository,
    SystemMappingUpdatesRepository,
)
from schemas.system_mapping_schema import SystemMappingCurrent, SystemMappingUpdates
from api.requests.system_mapping_requests import (
    CreateNewSystemMapLive,
    CreateSystemMapUpdate,
    UpdateSystemMapUpdate,
)
from typing import List


class SystemMappingService:
    def __init__(self, db: Session):
        self.repository = SystemMappingRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SystemMappingCurrent]:
        query = self.repository.get_all(skip, limit)
        # return [SystemMappingCurrent.from_db(el) for el in query]
        return query

    def get_by_hydraulic_name(self, hydraulic_name: str) -> SystemMappingCurrent:
        query = self.repository.get_by_hydraulic_name(hydraulic_name)
        # return SystemMappingCurrent.from_db(query)
        return query
    
    def create_new_entry(self, new_sys_map: CreateNewSystemMapLive) -> SystemMappingCurrent:
        new_sys_map_obj = self.repository.create_new_entry(new_obj=new_sys_map)
        # return SystemMappingCurrent.from_db(new_sys_map_obj)
        return new_sys_map_obj
    
        

class SystemMappingUpdateService:
    def __init__(self, db: Session):
        self.repository = SystemMappingUpdatesRepository(db)
 
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SystemMappingUpdates]:
        query = self.repository.get_all(skip, limit)
        # return [SystemMappingUpdates.from_db(el) for el in query]
        return query

    def get_by_hydraulic_name(self, hydraulic_name: str) -> SystemMappingUpdates:
        query = self.repository.get_by_hydraulic_name(hydraulic_name)
        # return SystemMappingUpdates.from_db(query)
        return query

    def create_new_update(self, new_sys_map: CreateSystemMapUpdate) -> SystemMappingUpdates:
        new_sys_map_obj = self.repository.create_new_update(new_entry=new_sys_map)
        # return SystemMappingUpdates.from_db(new_sys_map_obj)
        return new_sys_map_obj

    def update_existing_entry(
        self, update_id: int, modified_sys_map: UpdateSystemMapUpdate
    ) -> SystemMappingUpdates:
        modified_sys_map_obj = self.repository.updated_existing_entry(
            update_id, modified_sys_map
        )
        # return SystemMappingUpdates.from_db(modified_sys_map_obj)
        return modified_sys_map_obj
