from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DB_PATH = "app_data/audit.db"

class Base(DeclarativeBase):
    pass

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    policy_name: Mapped[str] = mapped_column(String(200))
    security_level: Mapped[str] = mapped_column(String(32))
    context_hash: Mapped[str] = mapped_column(String(64))
    risk_score: Mapped[float] = mapped_column(Float)
    decision: Mapped[str] = mapped_column(String(32))
    directive_json: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(String, nullable=True)

_engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
Base.metadata.create_all(_engine)


def context_hash_of(obj) -> str:
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def add_audit_entry(*, policy_name: str, security_level: str, context_obj, risk_score: float, decision: str, directive_obj=None, error: Optional[str] = None) -> None:
    ts = datetime.now(timezone.utc)
    ch = context_hash_of(context_obj)
    directive_json = json.dumps(directive_obj) if directive_obj is not None else None
    with Session(_engine) as session:
        session.add(AuditLog(
            timestamp_utc=ts,
            policy_name=policy_name,
            security_level=security_level,
            context_hash=ch,
            risk_score=risk_score,
            decision=decision,
            directive_json=directive_json,
            error=error
        ))
        session.commit()
