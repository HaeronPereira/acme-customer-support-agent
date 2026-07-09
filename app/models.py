from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    industry = Column(String(100), nullable=False)
    contact_name = Column(String(100), nullable=False)
    contact_email = Column(String(120), nullable=False)
    account_manager = Column(String(100), nullable=False)
    status = Column(String(30), default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)

    issues = relationship(
        "Issue",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Issue(Base):
    __tablename__ = "issues"

    issue_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), nullable=False)
    status = Column(String(30), default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="issues")

    updates = relationship(
        "IssueUpdate",
        back_populates="issue",
        cascade="all, delete-orphan"
    )

    next_actions = relationship(
        "NextAction",
        back_populates="issue",
        cascade="all, delete-orphan"
    )


class IssueUpdate(Base):
    __tablename__ = "issue_updates"

    update_id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(
        Integer,
        ForeignKey("issues.issue_id"),
        nullable=False
    )

    updated_by = Column(String(100), nullable=False)
    update_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    issue = relationship("Issue", back_populates="updates")


class NextAction(Base):
    __tablename__ = "next_actions"

    action_id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(
        Integer,
        ForeignKey("issues.issue_id"),
        nullable=False
    )

    action = Column(Text, nullable=False)
    owner = Column(String(100), nullable=False)
    status = Column(String(30), default="Pending")
    due_date = Column(DateTime)

    issue = relationship("Issue", back_populates="next_actions")


class AppUser(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    keycloak_id = Column(
        String(100),
        unique=True,
        nullable=True,
    )

    preferred_customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=True
    )

    customer = relationship("Customer")