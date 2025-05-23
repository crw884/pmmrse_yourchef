from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import User
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='static/img', default="static/img/default.png" , blank=True, null=True)
    prep_time = models.PositiveIntegerField(help_text="Время готовки в минутах",default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through='RecipeTag')
    #updated_at = models.DateTimeField(auto_now=True) #????
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    slug = models.SlugField(max_length=100, unique=True)

    rating = models.PositiveIntegerField(default=0, editable=True)
    rating_count = models.PositiveIntegerField(default=0, editable=True)

    def update_rating(self, newrating, up):
        if up:
            self.rating_count += 1
            self.rating += newrating
        else:
            self.rating_count -= 1
            self.rating -= newrating
        self.save(update_fields=['rating', 'rating_count'])

    def get_rating(self):
        if self.rating_count == 0:
            return 0
        return  self.rating / self.rating_count

    def __str__(self):
        return self.title

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='static/img', blank=True, null=True)
    class Meta:
        ordering = ['step_number']
        unique_together = ('recipe', 'step_number')
    def __str__(self):
        return f"Шаг {self.step_number} для {self.recipe.title}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    description = models.TextField(blank=True,help_text="Информация об ингредиенте")
    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.ingredient.name} в {self.recipe.title}"

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'tag')

    def __str__(self):
        return f"{self.tag.name} для {self.recipe.title}"

class RecipeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_ratings')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Рейтинг от 1 до 5"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   # updated_at = models.DateTimeField(auto_now=True) ??
    class Meta:
         unique_together = ('recipe', 'user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.update_rating(newrating = self.rating, up=True)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.recipe.update_rating(newrating=self.rating, up=False)

    def __str__(self):
        return f"{self.rating}/5 от {self.user.username} для {self.recipe.title}"