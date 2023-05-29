from apps.property.models import Property


class PropertyService:

    def create(self, validated_data):
        return Property.objects.create(**validated_data)



property_service = PropertyService()