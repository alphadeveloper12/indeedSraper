from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_description_html = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    company_link = models.CharField(max_length=10000, blank=True, null=True)
    last_date = models.DateField()
    job_type = models.CharField(max_length=50)
    salary = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    apply_link = models.TextField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    written_by = models.CharField(max_length=100)
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Additional fields
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='blogs', blank=True)

    def __str__(self):
        return self.title
