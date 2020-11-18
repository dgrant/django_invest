# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="currency",
            options={"verbose_name_plural": "currencies"},
        ),
        migrations.RenameField(
            model_name="trade",
            old_name="numshares",
            new_name="number_of_shares",
        ),
    ]
