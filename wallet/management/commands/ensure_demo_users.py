from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from wallet.demo_sandbox import ensure_demo_users_exist, reset_demo_sandbox


class Command(BaseCommand):
    help = "Create demo guest + peer users if missing, then reset sandbox ledger (for local/testing)."

    def handle(self, *args, **options) -> None:
        try:
            ensure_demo_users_exist()
            reset_demo_sandbox()
        except ValueError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS("Demo sandbox users ensured and ledger reset."))
