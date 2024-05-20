# store/migrations/0014_subscriptionplan_alter_subscription_expirationdate_and_more.py

from django.db import migrations, models
import django.utils.timezone

def create_default_subscription_plan(apps, schema_editor):
    SubscriptionPlan = apps.get_model('store', 'SubscriptionPlan')
    SubscriptionPlan.objects.create(
        planID=1,
        name='Default Plan',
        price=0.0,
        description='This is a default subscription plan.'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_subscription_expirationdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('planID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='subscription',
            name='expirationDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.SubscriptionPlan'),
            preserve_default=False,
        ),
        migrations.RunPython(create_default_subscription_plan),
    ]