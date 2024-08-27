from django.urls import resolve
from django.urls import reverse

from isfahan.users.models import User


def test_user_detail(user: User):
    assert (
<<<<<<< HEAD
        reverse("api:user-detail", kwargs={"pk": user.pk}) == f"/api/users/{user.pk}/"
    )
    assert resolve(f"/api/users/{user.pk}/").view_name == "api:user-detail"
=======
        reverse("api:user-detail", kwargs={"username": user.username})
        == f"/api/users/{user.username}/"
    )
    assert resolve(f"/api/users/{user.username}/").view_name == "api:user-detail"
>>>>>>> seya/apiv1.0


def test_user_list():
    assert reverse("api:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:user-list"


def test_user_me():
    assert reverse("api:user-me") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:user-me"
