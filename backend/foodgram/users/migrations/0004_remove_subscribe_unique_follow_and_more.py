# Generated by Django 4.2.1 on 2023-06-11 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_subscribe_prevent_self_follow_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='unique_follow',
        ),
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='prevent_self_follow',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='Данная подписка уже существует'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.CheckConstraint(check=models.Q(('author', models.F('user')), _negated=True), name='Нельзя подписаться на самого себя'),
        ),
    ]
