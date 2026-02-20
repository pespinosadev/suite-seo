from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_role
from app.modules.topics import schemas, service

router = APIRouter()


# ── Auto topics ──────────────────────────────────────────────

@router.get("/auto", response_model=list[schemas.AutoTopicOut])
async def list_auto_topics(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.list_auto_topics(db)


@router.post("/auto", response_model=schemas.AutoTopicOut, status_code=status.HTTP_201_CREATED)
async def create_auto_topic(
    body: schemas.AutoTopicCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.create_auto_topic(body, db)


@router.put("/auto/{auto_id}", response_model=schemas.AutoTopicOut)
async def update_auto_topic(
    auto_id: int,
    body: schemas.AutoTopicUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.update_auto_topic(auto_id, body, db)


@router.delete("/auto/{auto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_auto_topic(
    auto_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    await service.delete_auto_topic(auto_id, db)


@router.post("/auto/apply", response_model=list[schemas.DailyTopicOut], status_code=status.HTTP_201_CREATED)
async def apply_auto_topics(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.apply_auto_topics(db)


# ── Categories ──────────────────────────────────────────────

@router.get("/categories", response_model=list[schemas.TopicCategoryOut])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.list_categories(db)


@router.post("/categories", response_model=schemas.TopicCategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    body: schemas.TopicCategoryCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.create_category(body, db)


@router.put("/categories/{cat_id}", response_model=schemas.TopicCategoryOut)
async def update_category(
    cat_id: int,
    body: schemas.TopicCategoryCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.update_category(cat_id, body, db)


@router.delete("/categories/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    cat_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    await service.delete_category(cat_id, db)


# ── Daily topics ──────────────────────────────────────────────

@router.get("/added", response_model=list[schemas.DailyTopicOut])
async def list_topics(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.list_topics(db)


@router.post("/added", response_model=schemas.DailyTopicOut, status_code=status.HTTP_201_CREATED)
async def create_topic(
    body: schemas.DailyTopicCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.create_topic(body, db)


@router.put("/added/{topic_id}", response_model=schemas.DailyTopicOut)
async def update_topic(
    topic_id: int,
    body: schemas.DailyTopicUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.update_topic(topic_id, body, db)


@router.delete("/added/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    await service.delete_topic(topic_id, db)


# ── Email ──────────────────────────────────────────────

@router.post("/send", status_code=status.HTTP_200_OK)
async def send_email(
    body: schemas.SendEmailRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await service.send_topics_email(
        body.recipients, body.subject, body.html_body, db,
        sender_email=current_user.email,
    )
    return {"ok": True}
