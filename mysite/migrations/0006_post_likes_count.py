# Generated by Django 4.1.5 on 2023-01-20 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("mysite", "0005_alter_post_user")]

    operations = [
        migrations.AddField(
            model_name="post", name="likes_count", field=models.IntegerField(default=0)
        )
    ]
