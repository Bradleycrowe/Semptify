from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter(prefix="/test")

@router.get("/simple")
async def test_simple():
    return {"status": "works"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
