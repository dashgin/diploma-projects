from fastapi import APIRouter, Depends

from app import crud
from app.api.deps import SessionDep, get_current_user
from app.models import KnowledgeAreaRead

router = APIRouter(prefix="/areas", tags=["areas"])


@router.get("/", dependencies=[Depends(get_current_user)])
def read_areas(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> list[KnowledgeAreaRead]:
    """
    Retrieve knowledge areas.
    """
    areas = crud.get_areas(session=session, skip=skip, limit=limit)
    return areas
