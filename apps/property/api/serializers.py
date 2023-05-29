from rest_framework import serializers


class PropertySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250, required=True)
    bio = serializers.CharField(max_length=1000, required=False)
    owner = serializers.UUIDField(required=False)
    tenant = serializers.UUIDField(required=False)

    class Meta:
        fields = ('id', 'name', 'bio', 'owner', 'tenant')

