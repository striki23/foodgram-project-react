from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=100
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10
    )

    def __str__(self):
        #return f'{self.name} {self.measurement_unit}'
        return self.name
        
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True)
    color = models.CharField(
        max_length=7,
        default='#FF0000',
        unique=True
    )
    slug = models.SlugField(unique=True,
                            verbose_name='тег')
    
    def __str__(self):
            return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Recipe(models.Model):
    name = models.CharField(
        'Название рецепта',
        max_length=100,
        help_text='Введите название рецепта'
        )
    text = models.TextField(
        'Описание приготовления',
        help_text='Введите текст поста'
        )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_posts'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountIngredient'
    )

    tags =  models.ManyToManyField(Tag)

    image = models.ImageField(
        'Фото блюда',
        upload_to='recipes/images/',
        blank=True
    )

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator(1)],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

class AmountIngredient(models.Model):
    """Количество ингредиентов в блюде.
    Модель связывает Recipe и Ingredient с указанием количества ингредиента.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='В каких рецептах',
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Связанные ингредиенты',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0
    )
        # validators=(
        #     MinValueValidator(
        #         Limits.MIN_AMOUNT_INGREDIENTS,
        #         'Нужно хоть какое-то количество.',
        #     ),
        #     MaxValueValidator(
        #         Limits.MAX_AMOUNT_INGREDIENTS,
        #         'Слишком много!',
        #     ),
        # ),
    

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe', )
        # constraints = (
        #     UniqueConstraint(
        #         fields=('recipe', 'ingredients', ),
        #         name='\n%(app_label)s_%(class)s ingredient alredy added\n',
        #     ),
        # )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'
    
    