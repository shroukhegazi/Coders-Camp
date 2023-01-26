# Generated by Django 4.1.5 on 2023-01-26 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("mysite", "0009_like_user")]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="mysite.post"
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="post",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="mysite.post",
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
