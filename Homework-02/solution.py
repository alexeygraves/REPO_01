import re
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ConfigDict


class UserRegistration(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str
    password_confirm: str = Field(exclude=True)
    age: int = Field(ge=18, le=120)
    registration_date: datetime = Field(default_factory=datetime.now)
    # задание 2: добавил full_name и phone
    full_name: str
    phone: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("username может содержать только латинские буквы, цифры и символ подчёркивания")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        if not re.search(r'\d', v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r'[a-z]', v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        return v

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if len(v) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")
        if not v[0].isupper():
            raise ValueError("Имя должно начинаться с заглавной буквы")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        # +X-XXX-XX-XX — ровно такой формат, без вариаций
        if not re.match(r'^\+\d-\d{3}-\d{2}-\d{2}$', v):
            raise ValueError("Телефон должен быть в формате +X-XXX-XX-XX")
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        return self


def register_user(data: dict) -> Union[UserRegistration, list]:
    try:
        user = UserRegistration(**data)
        return user
    except Exception as e:
        errors = []
        for err in e.errors():
            field = " -> ".join(str(loc) for loc in err["loc"])
            errors.append(f"{field}: {err['msg']}")
        return errors


# задание 3: рекурсивная модель с произвольной вложенностью

class Node(BaseModel):
    data: str
    child: Optional["Node"] = None

# нужно явно вызвать rebuild иначе forward ref не резолвится
Node.model_rebuild()


def build_nested(depth: int, data_value: str = "any_data") -> Node:
    if depth <= 0:
        return Node(data=data_value)
    return Node(data=data_value, child=build_nested(depth - 1, data_value))


if __name__ == "__main__":
    good_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "Secret123",
        "password_confirm": "Secret123",
        "age": 25,
        "full_name": "John",
        "phone": "+7-999-12-34"
    }
    result = register_user(good_data)
    if isinstance(result, list):
        print("errors:", result)
    else:
        # password_confirm не попадает в вывод — exclude=True в Field
        print(result.model_dump_json(indent=2))

    bad_data = {
        "username": "j!",
        "email": "notanemail",
        "password": "weak",
        "password_confirm": "mismatch",
        "age": 15,
        "full_name": "a",
        "phone": "89991234"
    }
    errors = register_user(bad_data)
    print("\nvalidation errors:")
    for e in errors:
        print(" -", e)

    # TODO: потом добавить обёртку под FastAPI endpoint, сейчас просто функция
    node = build_nested(3)
    print("\nnested json:")
    print(node.model_dump_json(indent=2))
