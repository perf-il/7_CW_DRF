from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import Habit
from habits.pagination import HabitListPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitListPagination

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()

    def list(self, request, *args, **kwargs):
        #  проверка пользователя: администратор видит все привычки, остальные только публичные и свои
        if self.request.user.is_superuser:
            queryset = Habit.objects.all()
        else:
            queryset = Habit.objects.filter(is_public=True) | Habit.objects.filter(user=self.request.user.pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]