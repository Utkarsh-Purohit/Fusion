from rest_framework import viewsets, filters
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from ..models import Item, DepartmentInfo, SectionInfo, InventoryRequest, ReturnedItem
from .serializers import (
    ItemSerializer, 
    DepartmentInfoSerializer, 
    SectionInfoSerializer,
    InventoryRequestSerializer,
    ReturnedItemSerializer
)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class DepartmentInfoViewSet(viewsets.ModelViewSet):
    queryset = DepartmentInfo.objects.all()
    serializer_class = DepartmentInfoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['department_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department', None)
        if department:
            # Case-insensitive filtering
            queryset = queryset.filter(department_name__iexact=department)
        else:
            # Return an empty queryset if no department is provided
            queryset = queryset.none()
        return queryset

class SectionInfoViewSet(viewsets.ModelViewSet):
    queryset = SectionInfo.objects.all()
    serializer_class = SectionInfoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['section_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        section = self.request.query_params.get('section', None)
        if section:
            # Case-insensitive filtering
            queryset = queryset.filter(section_name__iexact=section)
        else:
            # Return an empty queryset if no section is provided
            queryset = queryset.none()
        return queryset

class InventoryRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing InventoryRequest objects.
    """
    queryset = InventoryRequest.objects.all()
    serializer_class = InventoryRequestSerializer
    permission_classes = [IsAuthenticated]

class ItemCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Aggregating total quantity for departments and sections
            department_total = DepartmentInfo.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            section_total = SectionInfo.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

            return Response({
                "department_total_quantity": department_total,
                "section_total_quantity": section_total,
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class ReturnProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Extract data from request
        item_name = request.data.get('item_name')
        quantity_returned = request.data.get('quantity_returned')
        department_name = request.data.get('department_name', None)
        section_name = request.data.get('section_name', None)

        if not item_name or not quantity_returned:
            return Response(
                {"error": "Item name and quantity returned are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to fetch the item
        item = None
        if department_name:
            item = DepartmentInfo.objects.filter(
                item_name=item_name, 
                department_name=department_name
            ).first()
        elif section_name:
            item = SectionInfo.objects.filter(
                item_name=item_name, 
                section_name=section_name
            ).first()

        if not item:
            return Response(
                {"error": "Item not found in specified department/section."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate quantity
        if item.quantity < quantity_returned:
            return Response(
                {"error": "Return quantity exceeds available quantity."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update inventory
        item.quantity -= quantity_returned
        item.save()

        # Create return record
        returned_item = ReturnedItem.objects.create(
            item_name=item_name,
            quantity_returned=quantity_returned,
            department_name=department_name,
            section_name=section_name,
            price=item.price,
            specifications=item.specifications
        )

        return Response(
            ReturnedItemSerializer(returned_item).data,
            status=status.HTTP_201_CREATED
        )
    def get(self, request, *args, **kwargs):
        """
        List ALL returned items (regardless of approval status)
        """
        returned_items = ReturnedItem.objects.all()  # Removed the approval_status filter
        serializer = ReturnedItemSerializer(returned_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)