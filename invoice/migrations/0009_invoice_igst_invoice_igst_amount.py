# Generated by Django 4.1.5 on 2023-07-30 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0008_alter_invoice_particular_invoice"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="igst",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="invoice",
            name="igst_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
