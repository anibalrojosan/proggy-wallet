from __future__ import annotations

import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from wallet.demo_sandbox import is_demo_guest_user, reset_demo_sandbox, tear_down_demo_sandbox

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def reset_demo_on_guest_login(sender, request, user, **kwargs) -> None:
    if is_demo_guest_user(user):
        try:
            reset_demo_sandbox()
        except Exception:
            logger.exception("reset_demo_sandbox failed after guest login")


@receiver(user_logged_out)
def remove_demo_users_on_guest_logout(sender, request, user, **kwargs) -> None:
    if user is not None and is_demo_guest_user(user):
        try:
            tear_down_demo_sandbox()
        except Exception:
            logger.exception("tear_down_demo_sandbox failed after guest logout")
