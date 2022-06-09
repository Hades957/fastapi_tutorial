from enum import Enum
from fastapi import APIRouter

app03 = APIRouter()

"""Path Parameters and Number Validations 路径参数和数字验证"""


@app03.get("/path/parameters")
async def path_params01():
    return {"message": "This is a message"}


# 函数的顺序就是路由的顺序
@app03.get("/path/{parameters}")
async def path_params01(parameters: str):
    return {"message": parameters}


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get("/enum/{city}")  # 枚举类型参数
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 1492, "death": 7}
    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 1492, "death": 8}
    return {"city_name": city, "latest": "unknown"}
