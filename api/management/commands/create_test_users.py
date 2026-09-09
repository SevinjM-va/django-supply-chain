from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = "Create two test user accounts"

    def handle(self, *args, **options):
        users = [
            {
                "username": "student1",
                "email": "student1@example.com",
                "password": "Student123!",
                "user_type": User.UserType.CONSUMER,
            },
            {
                "username": "student2",
                "email": "student2@example.com",
                "password": "Student123!",
                "user_type": User.UserType.SUPPLIER,
            },
        ]

        for user_data in users:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "user_type": user_data["user_type"],
                },
            )

            if created:
                user.set_password(user_data["password"])
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {user.username} "
                        f"({user.user_type})"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {user.username}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Test users setup completed.")
        )