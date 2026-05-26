from django.db import models
from django.utils.text import slugify


class Lake(models.Model):
    POLLUTION_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    ecology_info = models.TextField(blank=True, verbose_name='Ecological Importance',
                                    help_text='Describe the ecological importance of this lake.')
    current_status = models.TextField(blank=True, help_text='Describe the current condition of the lake.')
    cleanup_needs = models.TextField(blank=True, verbose_name='Clean-up Needs',
                                     help_text='Describe what clean-up activities are needed.')
    area_sq_km = models.FloatField(null=True, blank=True, verbose_name='Area (sq km)')
    pollution_level = models.CharField(max_length=20, choices=POLLUTION_LEVELS, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Lake.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def hero_photo(self):
        return self.photos.first()


class LakePhoto(models.Model):
    PHOTO_TYPES = [
        ('before', 'Before Clean-up'),
        ('after', 'After Clean-up'),
        ('general', 'General'),
    ]
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='lake_photos/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Or provide an external image URL')
    caption = models.CharField(max_length=300, blank=True)
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPES, default='general')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lake.name} photo"

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''
