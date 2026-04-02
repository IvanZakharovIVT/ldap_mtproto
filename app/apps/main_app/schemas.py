from typing import Annotated, Optional

from pydantic import BaseModel, Field


class UserAuthSchemaBase(BaseModel):
    username: Annotated[str, Field()]
    password: Annotated[str, Field()]


class UserSchema(BaseModel):
    username: Annotated[str, Field()]
    tg_link: Optional[Annotated[str, Field()]] = None
