# Generated by Django 4.1.5 on 2023-01-20 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("mysite", "0001_initial")]

    operations = [
        migrations.RenameField(model_name="post", old_name="user_id", new_name="user")
    ]
