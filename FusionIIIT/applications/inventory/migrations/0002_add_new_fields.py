from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),  # Your initial migration
    ]

    operations = [
        # DepartmentInfo fields
        migrations.AddField(
            model_name='departmentinfo',
            name='specifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='departmentinfo',
            name='date_of_purchase',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='departmentinfo',
            name='indent_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='departmentinfo',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        
        # SectionInfo fields
        migrations.AddField(
            model_name='sectioninfo',
            name='specifications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sectioninfo',
            name='date_of_purchase',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sectioninfo',
            name='indent_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='sectioninfo',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]