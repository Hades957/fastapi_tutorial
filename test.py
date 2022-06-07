from pydantic import BaseModel


class A(BaseModel):
  prop1: str
  prop2: str


class B(BaseModel):
  a: A


data = {
  'prop1': 'some value',
  'prop2': 'some other value'
}

b = B(a=A(**data))

print(b)