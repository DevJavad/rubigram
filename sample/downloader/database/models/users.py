from tortoise.fields import IntField, CharField
from tortoise.models import Model


class Users(Model):
    id = IntField(pk=True)
    user_id = CharField(max_length=50, unique=True)

    class Meta:
        table = "users"

    def __repr__(self):
        return "Users(user_id={})".format(self.user_id)