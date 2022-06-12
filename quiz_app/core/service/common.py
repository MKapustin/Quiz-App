import pydantic
import fastapi.encoders as encoders


class Schema(pydantic.BaseModel):
    class Config:
        orm_mode = True

    def serialize(self):
        return encoders.jsonable_encoder(self)
