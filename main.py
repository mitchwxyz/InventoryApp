from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import api, webapp, demo


app = FastAPI()

app.include_router(api.router)
app.include_router(webapp.router)
app.include_router(demo.router)

@app.get("/")
async def root():
    return RedirectResponse("/app/")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, log_level='debug')