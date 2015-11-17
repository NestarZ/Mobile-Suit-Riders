# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid_creation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grid',
            old_name='M',
            new_name='column_size',
        ),
        migrations.RenameField(
            model_name='grid',
            old_name='N',
            new_name='line_size',
        ),
        migrations.RenameField(
            model_name='grid',
            old_name='O',
            new_name='obstacle_amount',
        ),
    ]
