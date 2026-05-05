from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def hello_world():
    """
    Sample endpoint to test Swagger.
    """
    return {"message": "Hello, Swagger!"}
