from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveFloat, PositiveInt


class User(BaseModel):
    id: PositiveInt | None = None
    name: str = Field(min_length=2)
    email: EmailStr

    model_config = ConfigDict(
        validate_assignment=True    # Revalidate entity when attributes changes
    )


class Order(BaseModel):
    id: PositiveInt | None = None
    name: str = Field(min_length=2)
    user_id: PositiveInt
    value: PositiveFloat

    model_config = ConfigDict(
        validate_assignment=True    # Revalidate entity when attributes changes
    )
