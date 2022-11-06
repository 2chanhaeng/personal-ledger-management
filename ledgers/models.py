from typing import Final
from django.db import models
from users.models import User


class Ledger(models.Model):
    user: Final = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ledgers",
    )
    amount: Final = models.IntegerField()
    memo: Final = models.TextField()
    info: Final = models.JSONField()
    created_at: Final = models.DateTimeField(auto_now_add=True)
    # 생성 시각과 실제 사용 시각 분리하면 더 좋을 듯
    deleted_at: Final = models.DateTimeField(null=True, blank=True)
