from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from foodgram.settings import MY_CONSTANTS

User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты. Список возможных ингредиентов задаются админом."""

    name = models.CharField(
        "Название ингредиента",
        max_length=MY_CONSTANTS["LENGTH_TAG_INGRED_NAME"],
    )
    measurement_unit = models.CharField(
        "Единица измерения", max_length=MY_CONSTANTS["LENGTH_MEASUREMENT_UNIT"]
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        unique_together = ("name", "measurement_unit")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Теги. Список возможных тегов задаются админом."""

    name = models.CharField(
        max_length=MY_CONSTANTS["LENGTH_TAG_INGRED_NAME"], unique=True
    )
    color = models.CharField(
        max_length=MY_CONSTANTS["LENGTH_HEX_COLOR"],
        default="#FF0000",
        unique=True,
    )
    slug = models.SlugField(unique=True, verbose_name="тег")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Рецепты"""

    name = models.CharField(
        "Название рецепта",
        max_length=100,
        help_text="Введите название рецепта",
    )
    text = models.TextField(
        "Описание приготовления", help_text="Введите текст поста"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipe_posts", verbose_name="Автор"
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="AmountIngredient"
    )

    tags = models.ManyToManyField(Tag)

    image = models.ImageField(
        "Фото блюда", upload_to="recipes/images/", blank=True
    )

    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления в минутах",
        validators=[MinValueValidator(1)],
    )

    def ingredients_names(self):
        return " %s" % (
            ", ".join(
                [ingredient.name for ingredient in self.ingredients.all()]
            )
        )

    ingredients_names.short_description = "Ingredients"

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """Количество ингредиентов в блюде.
    Модель связывает Recipe и Ingredient с указанием количества ингредиента.
    """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="В каких рецептах",
        related_name="recipe",
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name="Связанные ингредиенты",
        related_name="ingredient",
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество", default=0
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Количество ингредиентов"
        ordering = ("recipe",)

    def __str__(self) -> str:
        return f"{self.amount} {self.ingredients}"


class ChooseRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        verbose_name="Рецепт",
    )

    class Meta:
        abstract = True


class FavoriteRecipe(ChooseRecipe):
    """Избранные рецепты."""

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="uniq_favorite_user_recipe"
            ),
        )

    def __str__(self):
        return f"{self.user} -> {self.recipe}"


class ShoppingCart(ChooseRecipe):
    """Список покупок."""

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="uniq_shoppinf_cart_user_recipe",
            ),
        )

    def __str__(self):
        return f"{self.user} -> {self.recipe}"
