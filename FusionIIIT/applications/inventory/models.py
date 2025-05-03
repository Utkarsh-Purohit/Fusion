from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('Consumable', 'Consumable'),
        ('Non-Consumable', 'Non-Consumable'),
    ]
    
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)  # e.g., computer
    quantity = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.item_name


class DepartmentInfo(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)  # e.g., computer
    quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    # New fields
    specifications = models.TextField(
        blank=True, 
        null=True,
        help_text="Detailed specifications of the item"
    )
    date_of_purchase = models.DateField(
        blank=True, 
        null=True,
        help_text="Date when the item was purchased"
    )
    indent_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Purchase indent/reference number"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Price of the item",
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.department_name} - {self.item_name}"

    class Meta:
        verbose_name = "Department Inventory"
        verbose_name_plural = "Department Inventories"
        ordering = ['department_name', 'item_name']


class SectionInfo(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)  # e.g., computer
    quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    # New fields
    specifications = models.TextField(
        blank=True, 
        null=True,
        help_text="Detailed specifications of the item"
    )
    date_of_purchase = models.DateField(
        blank=True, 
        null=True,
        help_text="Date when the item was purchased"
    )
    indent_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Purchase indent/reference number"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Price of the item",
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.section_name} - {self.item_name}"

    class Meta:
        verbose_name = "Section Inventory"
        verbose_name_plural = "Section Inventories"
        ordering = ['section_name', 'item_name']


# -------------- NEW MODEL --------------
class InventoryRequest(models.Model):
    """
    Represents an inventory request made by a department for a particular item.
    """
    APPROVAL_CHOICES = [
        ('APPROVED', 'APPROVED'),
        ('NOT_APPROVED', 'NOT_APPROVED'),
        ('PENDING', 'PENDING'),
    ]

    request_id = models.AutoField(primary_key=True)
    date = models.DateField()
    item_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    purpose = models.TextField()
    specifications = models.TextField()
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default='PENDING'
    )

    def __str__(self):
        return f"{self.item.item_name} - {self.department.department_name} ({self.approval_status})"
