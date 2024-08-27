from isfahan.users.models import User


def test_user_get_absolute_url(user: User):
<<<<<<< HEAD
    assert user.get_absolute_url() == f"/users/{user.pk}/"
=======
    assert user.get_absolute_url() == f"/users/{user.username}/"
>>>>>>> seya/apiv1.0
