from django.contrib.auth.models import User
from django.db import models

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('user', 'follower')
    
    def __str__(self) -> str:
        return self.user.username

class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} requested to {self.to_user}"