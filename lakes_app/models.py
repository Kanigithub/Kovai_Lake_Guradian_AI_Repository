from django.db import models
from django.utils.text import slugify


class Lake(models.Model):
    POLLUTION_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    ecology_info = models.TextField(
        blank=True, verbose_name="Ecological Importance",
        help_text="Describe the ecological importance of this lake."
    )
    current_status = models.TextField(
        blank=True,
        help_text="Describe the current condition of the lake."
    )
    cleanup_needs = models.TextField(
        blank=True, verbose_name="Clean-up Needs",
        help_text="Describe what clean-up activities are needed."
    )
    area_sq_km = models.FloatField(null=True, blank=True, verbose_name="Area (sq km)")
    pollution_level = models.CharField(max_length=20, choices=POLLUTION_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def hero_photo(self):
        """Return the best available photo URL for use as a panoramic hero image."""
        photo = self.photos.filter(photo_type='general').first() or self.photos.first()
        return photo.get_image() if photo else None

    def __str__(self):
        return self.name


class LakePhoto(models.Model):
    PHOTO_TYPE_CHOICES = [
        ('before', 'Before Clean-up'),
        ('after', 'After Clean-up'),
        ('general', 'General'),
    ]
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='lake_photos/', null=True, blank=True)
    image_url = models.URLField(blank=True, help_text="Or provide an external image URL")
    caption = models.CharField(max_length=300, blank=True)
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPE_CHOICES, default='general')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

    def __str__(self):
        return f"{self.lake.name} — {self.get_photo_type_display()}: {self.caption}"
