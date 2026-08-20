from django.test import TestCase

from users.models import User
from .models import AuditLog
from .services import create_audit_log


class AuditLogTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

    def test_audit_log_creation(self):

        audit = create_audit_log(
            user=self.user,
            action=AuditLog.Action.CREATE,
            module=AuditLog.Module.SUPPLY_CHAIN,
            object_type="Demand",
            object_id=100,
            to_status="DRAFT",
            description="Demand created.",
        )

        self.assertEqual(
            AuditLog.objects.count(),
            1
        )

        self.assertEqual(
            audit.action,
            AuditLog.Action.CREATE
        )

        self.assertEqual(
            audit.object_id,
            "100"
        )

    def test_submit_demand_creates_audit(self):

        demand = Demand.objects.create(
            created_by=self.user,
            status="DRAFT",
        )

        #submit_demand(
         #   user=self.user,
          #  demand=demand,
        #)

        audit = AuditLog.objects.filter(
            object_type="Demand",
            object_id=str(demand.id),
            action=AuditLog.Action.SUBMIT,
        ).first()

        self.assertIsNotNone(audit)

        self.assertEqual(
            audit.from_status,
            "DRAFT"
        )

        self.assertEqual(
            audit.to_status,
            "SUBMITTED"
        )