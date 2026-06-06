from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    birth_info = models.CharField(max_length=150, blank=True)
    death_info = models.CharField(max_length=150, blank=True)
    key_theories = models.TextField(blank=True)
    academic_background = models.TextField(blank=True)
    legacy = models.TextField(blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Post by @{self.author.username} at {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author_name} on post {self.post.id}"

