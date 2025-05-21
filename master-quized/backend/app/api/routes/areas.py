from fastapi import APIRouter, Depends
from sqlmodel import func, select

from app import crud
from app.api.deps import SessionDep, get_current_user
from app.models import AreasPublic, KnowledgeArea

router = APIRouter(prefix="/areas", tags=["areas"])


@router.get("/", dependencies=[Depends(get_current_user)], response_model=AreasPublic)
def read_areas(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> AreasPublic:
    """
    Retrieve knowledge areas.
    """
    # Get the count
    count_statement = select(func.count()).select_from(KnowledgeArea)
    count = session.exec(count_statement).one()

    # Get paginated data
    areas = crud.get_areas(session=session, skip=skip, limit=limit)

    return AreasPublic(data=areas, count=count)
