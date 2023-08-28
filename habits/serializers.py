from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    def validate(self, data):

        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError(
                    'Вы не можете одновременно выбрать связанную привычку и указать вознаграждение')

        if data.get('execution_time'):
            if data.get('execution_time') > 120:
                raise serializers.ValidationError(
                        'Время на выполнение действия не должно превышать 120 секунд')

        if data.get('related_habit'):
            if not data.get('related_habit').is_enjoyable:
                raise serializers.ValidationError(
                        'В связанные привычки могут попадать только привычки с признаком приятной привычки')

        if data.get('is_enjoyable'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки')

        if data.get('periodicity') > 7:
            print('period')
            raise serializers.ValidationError(
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней')

        return data

    class Meta:
        model = Habit
        fields = '__all__'
