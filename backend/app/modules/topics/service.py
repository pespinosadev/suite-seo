import asyncio
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.topics.models import AutoTopic, TopicCategory, DailyTopic
from app.modules.topics.schemas import AutoTopicCreate, AutoTopicUpdate, TopicCategoryCreate, DailyTopicCreate, DailyTopicUpdate

AUTO_TOPICS_DEFAULT = [
    ("Calendario Laboral/Escolar 2025 en ZONA", 1),
    ("Cuando es el próximo puente en ZONA", 2),
    ("Tiempo en ZONA", 3),
]


async def seed_auto_topics(db: AsyncSession) -> None:
    for title, order in AUTO_TOPICS_DEFAULT:
        result = await db.execute(select(AutoTopic).where(AutoTopic.title == title))
        if not result.scalars().first():
            db.add(AutoTopic(title=title, display_order=order))
    await db.commit()


# ── Auto topics ──────────────────────────────────────────────

async def list_auto_topics(db: AsyncSession) -> list[AutoTopic]:
    result = await db.execute(select(AutoTopic).order_by(AutoTopic.display_order))
    return result.scalars().all()


async def create_auto_topic(data: AutoTopicCreate, db: AsyncSession) -> AutoTopic:
    auto = AutoTopic(title=data.title, display_order=data.display_order)
    db.add(auto)
    await db.commit()
    await db.refresh(auto)
    return auto


async def update_auto_topic(auto_id: int, data: AutoTopicUpdate, db: AsyncSession) -> AutoTopic:
    result = await db.execute(select(AutoTopic).where(AutoTopic.id == auto_id))
    auto = result.scalar_one_or_none()
    if not auto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tema automático no encontrado")
    if data.title is not None:
        auto.title = data.title
    if data.is_active is not None:
        auto.is_active = data.is_active
    if data.display_order is not None:
        auto.display_order = data.display_order
    await db.commit()
    await db.refresh(auto)
    return auto


async def delete_auto_topic(auto_id: int, db: AsyncSession) -> None:
    result = await db.execute(select(AutoTopic).where(AutoTopic.id == auto_id))
    auto = result.scalar_one_or_none()
    if not auto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tema automático no encontrado")
    await db.delete(auto)
    await db.commit()


async def apply_auto_topics(db: AsyncSession) -> list[DailyTopic]:
    # Resolve COMUNES category id
    cat_result = await db.execute(select(TopicCategory).where(TopicCategory.name == "COMUNES"))
    comunes = cat_result.scalar_one_or_none()
    comunes_id = comunes.id if comunes else None

    result = await db.execute(
        select(AutoTopic).where(AutoTopic.is_active == True).order_by(AutoTopic.display_order)
    )
    autos = result.scalars().all()
    ids = []
    for auto in autos:
        topic = DailyTopic(title=auto.title, category_id=comunes_id)
        db.add(topic)
        await db.flush()
        ids.append(topic.id)
    await db.commit()
    result = await db.execute(
        select(DailyTopic)
        .where(DailyTopic.id.in_(ids))
        .options(selectinload(DailyTopic.category))
        .order_by(DailyTopic.id)
    )
    return result.scalars().all()


FIXED_CATEGORIES = [
    ("COMUNES", 1), ("NACIONAL", 2), ("MADRID", 3), ("ANDALUCIA", 4),
    ("BALEARES", 5), ("CANARIAS", 6), ("CV/MURCIA", 7), ("ASTURIAS/GALICIA", 8),
    ("EXTREMADURA/ZAMORA", 9), ("CATALUNA/ARAGON", 10), ("INTERNACIONAL", 11),
    ("ECONOMIA", 12), ("DEPORTES", 13), ("REVISTAS", 14),
]


async def seed_fixed_categories(db: AsyncSession) -> None:
    for name, order in FIXED_CATEGORIES:
        result = await db.execute(select(TopicCategory).where(TopicCategory.name == name))
        cat = result.scalar_one_or_none()
        if not cat:
            db.add(TopicCategory(name=name, display_order=order, is_fixed=True))
        else:
            cat.is_fixed = True
            cat.display_order = order
    await db.commit()


# ── Categories ──────────────────────────────────────────────

async def list_categories(db: AsyncSession) -> list[TopicCategory]:
    # Temporales (is_fixed=False) primero, luego fijas ordenadas por display_order
    result = await db.execute(
        select(TopicCategory).order_by(
            TopicCategory.is_fixed.asc(),
            TopicCategory.display_order.asc(),
            TopicCategory.name.asc()
        )
    )
    return result.scalars().all()


async def create_category(data: TopicCategoryCreate, db: AsyncSession) -> TopicCategory:
    existing = await db.execute(select(TopicCategory).where(TopicCategory.name == data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Categoría ya existe")
    cat = TopicCategory(name=data.name, display_order=data.display_order)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def update_category(cat_id: int, data: TopicCategoryCreate, db: AsyncSession) -> TopicCategory:
    result = await db.execute(select(TopicCategory).where(TopicCategory.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    dup = await db.execute(
        select(TopicCategory).where(TopicCategory.name == data.name, TopicCategory.id != cat_id)
    )
    if dup.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Nombre ya en uso")
    cat.name = data.name
    cat.display_order = data.display_order
    await db.commit()
    await db.refresh(cat)
    return cat


async def delete_category(cat_id: int, db: AsyncSession) -> None:
    result = await db.execute(select(TopicCategory).where(TopicCategory.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    if cat.is_fixed:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Las categorías fijas no se pueden eliminar")
    # unlink topics instead of blocking
    topics = await db.execute(select(DailyTopic).where(DailyTopic.category_id == cat_id))
    for t in topics.scalars().all():
        t.category_id = None
    await db.delete(cat)
    await db.commit()


# ── Daily topics ──────────────────────────────────────────────

async def list_topics(db: AsyncSession) -> list[DailyTopic]:
    result = await db.execute(
        select(DailyTopic)
        .options(selectinload(DailyTopic.category))
        .order_by(DailyTopic.created_at.desc())
    )
    return result.scalars().all()


async def create_topic(data: DailyTopicCreate, db: AsyncSession) -> DailyTopic:
    if data.category_id:
        cat = await db.execute(select(TopicCategory).where(TopicCategory.id == data.category_id))
        if not cat.scalar_one_or_none():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    topic = DailyTopic(
        title=data.title,
        url=data.url,
        include_url=data.include_url,
        observation=data.observation,
        category_id=data.category_id,
        original_source=data.original_source,
        original_url=data.original_url,
    )
    db.add(topic)
    await db.commit()
    result = await db.execute(
        select(DailyTopic).where(DailyTopic.id == topic.id).options(selectinload(DailyTopic.category))
    )
    return result.scalar_one()


async def update_topic(topic_id: int, data: DailyTopicUpdate, db: AsyncSession) -> DailyTopic:
    result = await db.execute(
        select(DailyTopic).where(DailyTopic.id == topic_id).options(selectinload(DailyTopic.category))
    )
    topic = result.scalar_one_or_none()
    if not topic:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tema no encontrado")
    if data.title is not None:
        topic.title = data.title
    if data.url is not None:
        topic.url = data.url
    if data.include_url is not None:
        topic.include_url = data.include_url
    if data.observation is not None:
        topic.observation = data.observation
    if data.category_id is not None:
        cat = await db.execute(select(TopicCategory).where(TopicCategory.id == data.category_id))
        if not cat.scalar_one_or_none():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        topic.category_id = data.category_id
    await db.commit()
    result = await db.execute(
        select(DailyTopic).where(DailyTopic.id == topic_id).options(selectinload(DailyTopic.category))
    )
    return result.scalar_one()


async def delete_topic(topic_id: int, db: AsyncSession) -> None:
    result = await db.execute(select(DailyTopic).where(DailyTopic.id == topic_id))
    topic = result.scalar_one_or_none()
    if not topic:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tema no encontrado")
    await db.delete(topic)
    await db.commit()


# ── Email ──────────────────────────────────────────────

async def send_topics_email(
    recipients: list[str],
    subject: str,
    html_body: str,
    db: AsyncSession,
    sender_email: str = "",
    sender_smtp_password: str = "",
) -> None:
    from app.core.config import settings

    if not settings.SMTP_HOST:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SMTP no configurado en el servidor. Añade SMTP_HOST al .env del VPS.",
        )

    # Build SMTP auth user: derive username from sender email + configured domain
    # e.g. pespinosa@prensaiberica.es + renr.grupoepi.es → pespinosa@renr.grupoepi.es
    if sender_email and settings.SMTP_AUTH_DOMAIN:
        username_prefix = sender_email.split("@")[0]
        auth_user = f"{username_prefix}@{settings.SMTP_AUTH_DOMAIN}"
    else:
        auth_user = settings.SMTP_USER

    auth_password = sender_smtp_password or settings.SMTP_PASSWORD
    display_from = sender_email if sender_email else (settings.SMTP_FROM or auth_user)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = display_from
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    host, port = settings.SMTP_HOST, settings.SMTP_PORT

    def _send() -> None:
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            if auth_user:
                smtp.login(auth_user, auth_password)
            smtp.sendmail(display_from, recipients, msg.as_bytes())

    try:
        await asyncio.get_event_loop().run_in_executor(None, _send)
    except smtplib.SMTPException as exc:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=f"Error SMTP: {exc}")

    # Mark all draft topics as sent
    now = datetime.datetime.now(datetime.timezone.utc)
    result = await db.execute(select(DailyTopic).where(DailyTopic.is_draft == True))
    for topic in result.scalars().all():
        topic.is_draft = False
        topic.sent_at = now
    await db.commit()
