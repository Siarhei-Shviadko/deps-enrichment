from pydantic import BaseModel

__all__ = ["ConfiguredBaseModel"]


class ConfiguredBaseModel(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True
