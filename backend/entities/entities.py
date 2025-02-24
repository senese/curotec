from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    PositiveFloat,
    PositiveInt,
    SecretStr,
    field_serializer,
)


class User(BaseModel):
    id: PositiveInt | None = None
    name: str = Field(min_length=2)
    email: EmailStr
    password: SecretStr

    model_config = ConfigDict(
        validate_assignment=True  # Revalidate entity when attributes changes
    )

    @field_serializer('password', when_used='json')
    def dump_secret(self, v):
        return v.get_secret_value()


class Order(BaseModel):
    id: PositiveInt | None = None
    name: str = Field(min_length=2)
    user_id: PositiveInt
    value: PositiveFloat

    model_config = ConfigDict(
        validate_assignment=True  # Revalidate entity when attributes changes
    )
