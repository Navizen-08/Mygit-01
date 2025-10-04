from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player_profile')
    display_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.user.username

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    staff_note = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Admin: {self.user.username}"

# Simple question model for quiz page (optional extensible)
class Question(models.Model):
    text = models.CharField(max_length=512)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)
    correct = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return self.text

@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        # create a Player profile by default (you can toggle admin manually via admin site)
        Player.objects.get_or_create(user=instance)
        # AdminProfile only created when is_staff True
        if instance.is_staff:
            AdminProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_profiles(sender, instance, **kwargs):
    if hasattr(instance, 'player_profile'):
        instance.player_profile.save()
    if hasattr(instance, 'admin_profile'):
        instance.admin_profile.save()
