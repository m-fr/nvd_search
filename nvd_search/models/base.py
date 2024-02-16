from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class UtilBaseModel(BaseModel):
    """Pydantic BaseModel with custom configuration.

    This class is a subclass of pydantic's BaseModel. It is used to define custom configuration for pydantic models.
    """
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_assignment=True
    )
