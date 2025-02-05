from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé basé sur AbstractUser.
    """
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('mechanic', 'Mechanic'),
    )

    # Champ pour le rôle utilisateur
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client',
        verbose_name="Rôle de l'utilisateur"
    )

    # Groupes et permissions personnalisés
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="Les groupes auxquels appartient cet utilisateur.",
        verbose_name="groupes"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Permissions spécifiques pour cet utilisateur.",
        verbose_name="permissions d'utilisateur"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
