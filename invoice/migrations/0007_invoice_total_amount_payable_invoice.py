# Generated by Django 4.1.5 on 2023-05-22 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0006_invoice_cgst_amount_invoice_sgst_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="total_amount_payable_invoice",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
