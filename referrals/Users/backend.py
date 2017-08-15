from django.contrib.auth.backends import ModelBackend


# class MyCustomBackend():
#     def authenticate(self, username):
#         try:
#             return User.objects.get(username=username)
#         except User.DoesNotExist:
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None


class MyCustomBackend(ModelBackend):
    def authenticate(self, user, **kwargs):
        return user
