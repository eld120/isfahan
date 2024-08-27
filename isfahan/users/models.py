from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for isfahan.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    # email = EmailField(_("email address"), unique=True)
    # username = None  # type: ignore[assignment]
    
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    # objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


# class Positions(models.Model):
#     user = models.ForeignKey("users.User",  on_delete=models.CASCADE)
#     stock = models.ForeignKey("market.Stock",  on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField( max_digits=5, decimal_places=2) 
    
        
     

# class UserTransactions(models.Model):
#     user = models.ForeignKey("users.User",  on_delete=models.CASCADE, related_name="user")
#     stock = models.ForeignKey("market.Stock",  on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField( max_digits=5, decimal_places=2)
#     timestamp = models.DateTimeField( auto_now=False, auto_now_add=False)
#         return reverse("users:detail", kwargs={"username": self.username})
