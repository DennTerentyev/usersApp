from django.db.models.sql.aggregates import Count
from .models import User


def check_invite_codes(fn):
    def wrapped():
        count = User.objects.annotate(c=Count('invite_code'))
        return count
    return wrapped
