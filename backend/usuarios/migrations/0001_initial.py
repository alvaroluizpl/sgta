from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
