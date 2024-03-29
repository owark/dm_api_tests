from typing import Optional
from pydantic import BaseModel, Extra, StrictStr, Field


class ResetPasswordModel(BaseModel):
    class Config:
        extra = Extra.forbid

    login: Optional[StrictStr] = Field(None, description='Login')
    email: Optional[StrictStr] = Field(None, description='Email')
