from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_delete_animatedslide_alter_popupbanner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='category',
            field=models.CharField(
                choices=[
                    ('academic', 'Academic'),
                    ('admissions', 'Admissions'),
                    ('chapel', 'Chapel'),
                    ('jobs', 'Job Opportunities'),
                    ('finance', 'Finance'),
                    ('staff', 'Staff'),
                    ('general', 'General'),
                ],
                default='general',
                max_length=30,
            ),
        ),
    ]