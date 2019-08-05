# Generated by Django 2.0.5 on 2019-08-04 14:57

from django.db import migrations, models
import django.db.models.deletion
import image_cropping.admin


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstaUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nickname_user', models.CharField(max_length=100, unique=True)),
                ('email_user', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('image_id', models.ImageField(blank=True, upload_to='insta/photos')),
            ],
            bases=(image_cropping.admin.ImageCroppingMixin, models.Model),
        ),
        migrations.AddField(
            model_name='follows',
            name='follow_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_out', to='insta.InstaUser'),
        ),
        migrations.AddField(
            model_name='follows',
            name='man',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_im', to='insta.InstaUser'),
        ),
    ]
