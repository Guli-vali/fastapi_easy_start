from fastapi_users import models


class User(models.BaseUser):
    pass


class UserDB(User, models.BaseUserDB):
    pass
