import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_fridgeitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridgeitem',
            name='quantity',
            field=models.PositiveIntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
        migrations.AddConstraint(
            model_name='fridgeitem',
            constraint=models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name='fridgeitem_quantity_at_least_one',
            ),
        ),
        migrations.AddConstraint(
            model_name='fridgeitem',
            constraint=models.UniqueConstraint(
                fields=('owner', 'name', 'zone', 'unit', 'expiry_date'),
                name='unique_fridge_item_details_per_owner',
            ),
        ),
    ]
