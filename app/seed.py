from datetime import datetime, timedelta

from app.database import SessionLocal, create_tables
from app.models import (
    Customer,
    Issue,
    IssueUpdate,
    NextAction,
    AppUser,
)

CUSTOMERS = [
    {
        "name": "Nova Retail Ltd",
        "industry": "Retail",
        "contact_name": "Emma Wilson",
        "contact_email": "emma@novaretail.com",
        "account_manager": "Sarah Johnson",
    },
    {
        "name": "BluePeak Logistics",
        "industry": "Logistics",
        "contact_name": "Daniel Carter",
        "contact_email": "daniel@bluepeak.com",
        "account_manager": "Sarah Johnson",
    },
    {
        "name": "Vertex Manufacturing",
        "industry": "Manufacturing",
        "contact_name": "Michael Adams",
        "contact_email": "michael@vertexmfg.com",
        "account_manager": "James Walker",
    },
    {
        "name": "GreenWave Energy",
        "industry": "Energy",
        "contact_name": "Sophia Brown",
        "contact_email": "sophia@greenwave.com",
        "account_manager": "James Walker",
    },
    {
        "name": "Orion Financial",
        "industry": "Financial Services",
        "contact_name": "Olivia Harris",
        "contact_email": "olivia@orionfs.com",
        "account_manager": "David Clark",
    },
]

CUSTOMER_ISSUES = {
    "Nova Retail Ltd": [
        {
            "title": "Payment Gateway Timeout",
            "priority": "High",
            "description": "Customers are experiencing timeout errors during online checkout."
        },
        {
            "title": "Inventory Synchronization Failure",
            "priority": "Medium",
            "description": "Warehouse stock levels are not synchronizing with the online store."
        },
        {
            "title": "Customer Portal Login Failure",
            "priority": "Critical",
            "description": "Multiple users cannot log in to the customer portal."
        },
    ],

    "BluePeak Logistics": [
        {
            "title": "Shipment Tracking Delay",
            "priority": "High",
            "description": "Shipment tracking information is delayed by several hours."
        },
        {
            "title": "Route Optimization Service Offline",
            "priority": "Critical",
            "description": "Route planning service is unavailable for dispatchers."
        },
        {
            "title": "Email Notifications Not Sent",
            "priority": "Medium",
            "description": "Customers are not receiving shipment notification emails."
        },
    ],

    "Vertex Manufacturing": [
        {
            "title": "Production Dashboard Unavailable",
            "priority": "Critical",
            "description": "Factory managers cannot access the production dashboard."
        },
        {
            "title": "Machine Telemetry Missing",
            "priority": "High",
            "description": "Telemetry data is not updating for several production lines."
        },
        {
            "title": "Quality Inspection Reports Delayed",
            "priority": "Medium",
            "description": "Inspection reports are generated several hours late."
        },
    ],

    "GreenWave Energy": [
        {
            "title": "Smart Meter Data Missing",
            "priority": "High",
            "description": "Meter readings are missing for multiple commercial customers."
        },
        {
            "title": "Billing Calculation Error",
            "priority": "Critical",
            "description": "Monthly invoices contain incorrect energy usage calculations."
        },
        {
            "title": "Outage Alert Notifications Delayed",
            "priority": "Medium",
            "description": "Customers receive outage notifications long after incidents occur."
        },
    ],

    "Orion Financial": [
        {
            "title": "Loan Approval Workflow Stuck",
            "priority": "Critical",
            "description": "Loan applications remain in pending status indefinitely."
        },
        {
            "title": "Fraud Detection Alerts Missing",
            "priority": "High",
            "description": "High-risk transactions are not generating fraud alerts."
        },
        {
            "title": "Customer Onboarding Failure",
            "priority": "Medium",
            "description": "New customer onboarding stops during identity verification."
        },
    ],
}

UPDATES = [
    {
        "updated_by": "Support Team",
        "update_text": "Customer reported the issue through the support portal."
    },
    {
        "updated_by": "Support Engineer",
        "update_text": "Issue reproduced successfully and escalated to engineering."
    },
    {
        "updated_by": "Engineering Team",
        "update_text": "Root cause identified. Permanent fix is currently being implemented."
    }
]

NEXT_ACTION = {
    "action": "Schedule a customer review call and provide an implementation update.",
    "owner": "Support Team",
    "status": "Pending",
}

APP_USERS = [
    {
        "username": "alice",
        "full_name": "Alice Smith",
        "department": "Sales",
    },
    {
        "username": "bob",
        "full_name": "Bob Johnson",
        "department": "Support",
    },
    {
        "username": "admin",
        "full_name": "System Administrator",
        "department": "Operations",
    },
]

def seed_customers(db):
    customers = []

    for customer_data in CUSTOMERS:

        customer = Customer(
            name=customer_data["name"],
            industry=customer_data["industry"],
            contact_name=customer_data["contact_name"],
            contact_email=customer_data["contact_email"],
            account_manager=customer_data["account_manager"],
            status="Active"
        )

        db.add(customer)
        customers.append(customer)

    db.commit()

    for customer in customers:
        db.refresh(customer)

    return customers


def seed_issues(db, customers):
    issues = []

    for customer in customers:

        customer_issues = CUSTOMER_ISSUES.get(customer.name, [])

        for issue_data in customer_issues:

            issue = Issue(
                customer_id=customer.customer_id,
                title=issue_data["title"],
                description=issue_data["description"],
                priority=issue_data["priority"],
                status="Open"
            )

            db.add(issue)
            issues.append(issue)

    db.commit()

    for issue in issues:
        db.refresh(issue)

    return issues



def seed_issue_updates(db, issues):

    for issue in issues:

        for update in UPDATES:

            issue_update = IssueUpdate(
                issue_id=issue.issue_id,
                updated_by=update["updated_by"],
                update_text=update["update_text"]
            )

            db.add(issue_update)

    db.commit()


def seed_next_actions(db, issues):

    for issue in issues:

        action = NextAction(
            issue_id=issue.issue_id,
            action=NEXT_ACTION["action"],
            owner=NEXT_ACTION["owner"],
            status=NEXT_ACTION["status"],
            due_date=datetime.now() + timedelta(days=3)
        )

        db.add(action)

    db.commit()


def seed_app_users(db):

    customers = db.query(Customer).all()

    for index, user_data in enumerate(APP_USERS):

        user = AppUser(
            username=user_data["username"],
            full_name=user_data["full_name"],
            department=user_data["department"],
            preferred_customer_id=customers[index].customer_id
        )

        db.add(user)

    db.commit()


def seed_database():

    create_tables()

    db = SessionLocal()

    try:

        print("Cleaning existing data...")

        db.query(NextAction).delete(synchronize_session=False)
        db.query(IssueUpdate).delete(synchronize_session=False)
        db.query(Issue).delete(synchronize_session=False)
        db.query(AppUser).delete(synchronize_session=False)
        db.query(Customer).delete(synchronize_session=False)


        db.commit()

        print("Seeding customers...")
        customers = seed_customers(db)

        print("Seeding issues...")
        issues = seed_issues(db, customers)

        print("Seeding issue updates...")
        seed_issue_updates(db, issues)

        print("Seeding next actions...")
        seed_next_actions(db, issues)

        print("Seeding application users...")
        seed_app_users(db)

        print("Database seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()