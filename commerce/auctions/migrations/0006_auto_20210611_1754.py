# Generated by Django 3.2.4 on 2021-06-11 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bidobject', to='auctions.listing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='commentobject', to='auctions.listing'),
            preserve_default=False,
        ),
    ]
