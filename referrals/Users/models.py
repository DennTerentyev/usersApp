from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    parent = models.ForeignKey('self', null=True, blank=True)
    points = models.PositiveIntegerField(default=0)
    email_verified = models.BooleanField(default=False)
    confirmation_code = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(blank=True)
    invite_code = models.PositiveIntegerField(null=True, unique=True)
    without_invite_code = models.BooleanField(default=False)
    ref_id = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     try:
    #         this_avatar = User.objects.get(id=self.id)
    #         if this_avatar.avatar != self.avatar:
    #             this_avatar.avatar.delete(save=False)
    #     except:
    #         pass
    #     super(User, self).save(*args, **kwargs)

    def get_referrals(self):
        users = User.objects.filter(Users_user__ref_id=self.id).order_by('id')
        return users

    def get_own_referrals(self):
        if self.ref_id != 0:
            return User.objects.get(id=self.ref_id)
        else:
            return False
    #
    # @property
    # def has_inviter(self):
    #     if self.ref_id:
    #         return True
    #     else:
    #         return False
    #
    # def get_inviter(self):
    #     return User.objects.get(id=self.ref_id)
