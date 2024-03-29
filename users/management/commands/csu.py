from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            tg_user_name='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('8888')
        user.save()
