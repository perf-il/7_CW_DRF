from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from habits.models import Habit
from users.models import User


class HabitTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.ts',
            password='1111',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.test_time = datetime(2023, 5, 17, 12, 0, 0)

        self.habit = Habit.objects.create(
            user=self.user,
            location='test location',
            time=self.test_time,
            action='test action',
            periodicity=1,
        )

    def test_create_habit(self):
        """Тестирование создания новой привычки"""
        data = {
            'user': self.user.pk,
            'location': 'test location',
            'time': self.test_time,
            'action': 'test action',
            'periodicity': 1,
        }

        response = self.client.post(
            reverse('habits:habits-list'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(Habit.objects.all().count() == 2)

        self.assertEqual(
            response.json(),
            {
                 'id': 2,
                 'location': 'test location',
                 'time': '2023-05-17T12:00:00+03:00',
                 'action': 'test action',
                 'is_enjoyable': False,
                 'periodicity': 1,
                 'reward': None,
                 'execution_time': None,
                 'is_public': False,
                 'user': self.user.pk,
                 'related_habit': None
            }
        )

    def test_list_habits(self):
        """Тестирование списка привычек"""

        response = self.client.get(
            reverse('habits:habits-list')

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [
                {'id': self.habit.pk,
                 'location': 'test location',
                 'time': '2023-05-17T12:00:00+03:00',
                 'action': 'test action',
                 'is_enjoyable': False,
                 'periodicity': 1,
                 'reward': None,
                 'execution_time': None,
                 'is_public': True,
                 'user': self.user.pk,
                 'related_habit': None}
            ]
        )

    def test_update_habit(self):
        """Тестирование редактирования привычки"""

        data = {
            'location': 'Test update location',
            'action': 'Test update action',
            'user': self.user.pk,
            'time': self.test_time,
            'periodicity': 2,
        }

        response = self.client.put(
            reverse('habits:habits-detail', kwargs={"pk": self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['location'],
            'Test update location'
        )

        self.assertEqual(
            response.json()['action'],
            'Test update action'
        )

        self.assertEqual(
            response.json()['periodicity'],
            2
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки"""

        self.assertTrue(
            Habit.objects.all().exists()
        )

        self.client.delete(
            reverse('habits:habits-detail', kwargs={"pk": self.habit.pk}),
        )

        self.assertFalse(
            Habit.objects.all().exists()
        )

    def test_validations(self):
        """Тестирование валидации при создании привычки"""

        data = {
            'user': self.user.pk,
            'location': 'test location',
            'time': self.test_time,
            'action': 'test action',
            'periodicity': 10,
        }

        response = self.client.post(
            reverse('habits:habits-list'),
            data=data
        )

        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
        )

        data = {
            'user': self.user.pk,
            'location': 'test location',
            'time': self.test_time,
            'action': 'test action',
            'periodicity': 1,
            'execution_time': 160,
        }

        response = self.client.post(
            reverse('habits:habits-list'),
            data=data
        )

        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Время на выполнение действия не должно превышать 120 секунд'
        )

        data = {
            'user': self.user.pk,
            'location': 'test location',
            'time': self.test_time,
            'action': 'test action',
            'periodicity': 1,
            'reward': 'банан',
            'related_habit': self.habit.pk
        }

        response = self.client.post(
            reverse('habits:habits-list'),
            data=data
        )

        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Вы не можете одновременно выбрать связанную привычку и указать вознаграждение'
        )

        data = {
            'user': self.user.pk,
            'location': 'test location',
            'time': self.test_time,
            'action': 'test action',
            'periodicity': 1,
            'related_habit': self.habit.pk
        }

        response = self.client.post(
            reverse('habits:habits-list'),
            data=data
        )

        self.assertEqual(
            response.json()['non_field_errors'][0],
            'В связанные привычки могут попадать только привычки с признаком приятной привычки'
        )

        self.enjoyable_habit = Habit.objects.create(
            user=self.user,
            location='test location',
            time=self.test_time,
            action='test action',
            periodicity=1,
            is_enjoyable=True,
        )

        data = {
            'user': self.user.pk,
            'location': 'test location',
            'time': self.test_time,
            'action': 'test action',
            'periodicity': 1,
            'is_enjoyable': True,
            'related_habit': self.enjoyable_habit.pk
        }

        response = self.client.post(
            reverse('habits:habits-list'),
            data=data
        )

        self.assertEqual(
            response.json()['non_field_errors'][0],
            'У приятной привычки не может быть вознаграждения или связанной привычки'
        )
