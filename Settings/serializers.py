from rest_framework import serializers
from .models import (
    Function,
    PermissionGroup,
    Responsibility,
    Role,
    RoleAssignment,
    Service,
    TypeOfService,
)


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = "__all__"


class TypeOfServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfService
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    type_of_service = serializers.StringRelatedField()
    parent_service = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = "__all__"


class CreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = "__all__"


class PermissionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionGroup
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RoleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = "__all__"
