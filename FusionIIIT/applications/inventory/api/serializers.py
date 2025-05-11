from rest_framework import serializers
from applications.inventory.models import Item, DepartmentInfo, SectionInfo, InventoryRequest, ReturnedItem

# Serializer for Item
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_id', 'item_name', 'quantity', 'type', 'unit']  # Fields to serialize


# Serializer for DepartmentInfo
class DepartmentInfoSerializer(serializers.ModelSerializer):
    date_of_purchase = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = DepartmentInfo
        fields = [
            'department_id',
            'department_name', 
            'item_name',
            'quantity',
            'specifications',
            'date_of_purchase',
            'indent_id',
            'price'
        ]
        extra_kwargs = {
            'specifications': {'required': False, 'allow_blank': True},
            'indent_id': {'required': False, 'allow_blank': True}
        }

class SectionInfoSerializer(serializers.ModelSerializer):
    date_of_purchase = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = SectionInfo
        fields = [
            'section_id',
            'section_name',
            'item_name',
            'quantity',
            'specifications',
            'date_of_purchase',
            'indent_id',
            'price'
        ]
        extra_kwargs = {
            'specifications': {'required': False, 'allow_blank': True},
            'indent_id': {'required': False, 'allow_blank': True}
        }

# -------------- NEW SERIALIZER --------------
class InventoryRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for InventoryRequest model
    """
    class Meta:
        model = InventoryRequest
        fields = [
            'request_id',
            'date',
            'item_name',
            'department_name',
            'approval_status',
            'purpose',
            'specifications'
        ]
        # or simply: fields = '__all__'

# api/serializers.py

class ReturnedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnedItem
        fields = [
            'return_id', 'item_name', 'quantity_returned', 
            'department_name', 'section_name', 'return_date', 
            'specifications', 'price', 'approval_status'
        ]
