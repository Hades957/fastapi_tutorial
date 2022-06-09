import uvicorn
from fastapi import FastAPI
from tutorial import app03, app04, app05, app06, app07, app08

# 实例化一个FastAPI应用
app = FastAPI()
# 将子应用的接口路由导入到主应用中,prefix:路由前缀  tags:文档中的标题
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06')
app.include_router(app07, prefix='/chapter07')
app.include_router(app08, prefix='/chapter08')
if __name__ == '__main__':
    # 使用uvicorn启动应用
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
