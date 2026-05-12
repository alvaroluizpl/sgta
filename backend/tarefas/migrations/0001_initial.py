from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('status', models.CharField(
                    choices=[
                        ('ABERTA', 'Aberta'),
                        ('EM_ANDAMENTO', 'Em andamento'),
                        ('CONCLUIDA', 'Concluída'),
                        ('CANCELADA', 'Cancelada'),
                    ],
                    default='ABERTA',
                    max_length=20,
                )),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_entrega', models.DateField()),
            ],
        ),
    ]
