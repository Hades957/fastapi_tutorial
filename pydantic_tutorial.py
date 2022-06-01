from pydantic import BaseModel, ValidationError, constr
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

# pydantic具有对数据的验证和规范的作用
print("\033[31m1. --- Pydantic的基本用法。Pycharm可以安装Pydantic插件 ---\033[0m")


class User(BaseModel):
    id: int  # 没有默认值，必填字段
    name: str = "John Snow"  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None  # 选填字段的另一种表达
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转换成int类型


external_data = {
    "id": '123',  # "123"
    "signup_ts": "2022-12-22 12:22",
    "friends": [1, 2, '3'],  # '3'是可以int('3')的
}

# 如何把external_data传给User类？可以使用python解包的方式
user = User(**external_data)
print(user.id, user.friends)  # 实例化后调用属性
print(repr(user.signup_ts))  # repr方法返回一个对象的 string 格式
print(user.dict())  # dict() 函数用于创建一个字典

print("\033[31m2. --- 校验失败的处理 ---\033[0m")
try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, "not number"])
except ValidationError as e:
    print(e.json())

print("\033[31m3. --- 模型类的属性和方法 ---\033[0m")
print(user.dict())  # 通过字典解析
print(user.json())  # 使用json解析
print(user.copy())  # 这里是浅拷贝，拷贝方式解析
print(User.parse_obj(obj=external_data))  # 解析对象的方式
# 解析原生的数据
print(User.parse_raw('{"id": 123, "name": "John Snow", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}'))
# 解析文件的方式
# path = Path('C:\\Users\\zbife\\Desktop\\csv\\pydantic_tutorial.json')
path = Path('pydantic_tutorial.json')
path.write_text('{"id": 123, "name": "John Snow", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}')
print(User.parse_file(path))
# 会返回具体使用的数据格式的方案
print(user.schema())
print(user.schema_json())
# 不检验数据直接创建模型类，不建议在construct方法中传入未经验证的数据
user_data = {"id": "error", "name": "John Snow", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}
print(User.construct(**user_data))

# 查看User类的所有字段，定义模型的时候，所有字段都注明类型，字段顺序就不会乱
print(User.__fields__.keys())

print("\033[31m4. --- 递归模型 ---\033[0m")


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]


# 报黄表示未严格按照Sound的格式传递，结果不报错是因为能解析
dogs1 = Dog(birthday=date.today(), weight=6.66, sound=[{"sound": "wang wang ~"}, {"sound": "ying ying ~"}])
dogs2 = Dog(birthday=date.today(), weight=6.66,
            sound=[Sound(sound='wang wang ~'), Sound(sound='ying ying ~')])
s1 = Sound(sound="wang wang ~")
s2 = Sound(sound="ying ying ~")

dogs3 = Dog(birthday=date.today(), weight=4.4, sound=[s1, s2])
print(dogs1.dict())
print(dogs2.dict())
print(dogs3.dict())

print("\033[31m5. --- ORM模型：从类实例创建符合ORM对象的模型 ---\033[0m")

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    name='Testing',
    domains=['example.com', 'imooc.com']
)

print(CompanyMode.from_orm(co_orm))
