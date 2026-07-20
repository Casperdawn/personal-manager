from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_finance():
    return {"message": "Finance endpoint"}
