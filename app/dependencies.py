from fastapi import Query

def pagination(
    limit: int = Query(default=20, ge=1, le=100, description="Results per page"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip")
):
    return {"limit": limit, "offset": offset}
