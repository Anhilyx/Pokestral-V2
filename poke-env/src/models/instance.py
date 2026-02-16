from pydantic import BaseModel, ConfigDict


class Instanciator(BaseModel):
    """
    Represents informations required to create a game instance.

    Attributes:
        opponent (str|None): The name of the opponent. If None, it means any opponent. Defaults to None.
        username (str|None, optional): Username for authentication. If none is provided, will be logged as a guest. Defaults to None.
        password (str|None, optional): Password for authentication. If none is provided, a non-registered account will be used. If no username is provided, it will be ignored. Defaults to None.
    """

    opponent: str|None = None
    username: str|None = None
    password: str|None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "opponent": "YourAccountNameHere",
                "username": "Pokestral",
                "password": "SuperSecretPassword"
            }
        }
    )


class UUIDModel(BaseModel):
    """
    Represents the UUID of a game instance.

    Attributes:
        uuid (str): The UUID of the instance.
    """

    uuid: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "uuid": "1234567890abcdef1234567890abcdef"
            }
        }
    )