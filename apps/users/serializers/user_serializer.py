from rest_framework import serializers
from apps.users.models.user_model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Это включает все поля модели User в сериализатор

    def create(self, validated_data):
        # Дополнительная логика при создании пользователя, если необходимо
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Дополнительная логика при обновлении пользователя, если необходимо
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
