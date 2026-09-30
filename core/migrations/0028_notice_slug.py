from django.db import migrations, models
from django.utils.text import slugify


def populate_notice_slugs(apps, schema_editor):
    Notice = apps.get_model('core', 'Notice')
    used_slugs = set()

    for notice in Notice.objects.order_by('pk'):
        base_slug = slugify(notice.title) or 'notice'
        if base_slug.isdigit():
            base_slug = f'notice-{base_slug}'

        slug = base_slug
        if slug in used_slugs:
            slug = f'{base_slug}-{notice.pk}'

        suffix = 2
        while slug in used_slugs:
            slug = f'{base_slug}-{notice.pk}-{suffix}'
            suffix += 1

        Notice.objects.filter(pk=notice.pk).update(slug=slug)
        used_slugs.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_notice_job_opportunities_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.RunPython(populate_notice_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='notice',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]