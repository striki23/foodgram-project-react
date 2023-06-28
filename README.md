# Сайт Foodgram «Продуктовый помощник»

![example workflow](https://github.com/striki23/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)

---
## **Адрес проекта**
http://84.252.141.69/admin/ Панель администратора<br>
http://84.252.141.69/api/docs/ Документация<br>
http://84.252.141.69/signin Вход на сайт и регистрация<br>
http://84.252.141.69/recipes Главная страница рецептов<br>
http://84.252.141.69/subscriptions Подписки<br>
http://84.252.141.69/recipes/create Создание рецепта<br>
http://84.252.141.69/favorites Избранное<br>
http://84.252.141.69/cart Список покупок

---
## Техническое описание проекта
Сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать и скачивать список продуктов, которые нужно купить для приготовления выбранных блюд.


### Сервисы и страницы проекта
#### Главная страница
Содержимое главной страницы — список первых шести рецептов, отсортированных по дате публикации (от новых к старым). Остальные рецепты доступны на следующих страницах: внизу страницы есть пагинация.

#### Страница рецепта
На странице — полное описание рецепта. Для авторизованных пользователей — возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

#### Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

#### Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.

- Сценарий поведения пользователя:

Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался. Сортировка записей — по дате публикации (от новых к старым)
При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

#### Список избранного
Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.

- Сценарий поведения пользователя:

Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
При необходимости пользователь может удалить рецепт из избранного.

#### Список покупок
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

- Сценарий поведения пользователя:

Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
При необходимости пользователь может удалить рецепт из списка покупок. Список покупок скачивается в формате .txt (или, по желанию, можно сделать выгрузку PDF).
При скачивании списка покупок ингредиенты в результирующем списке не должны дублироваться; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке должен быть один пункт: Сахар — 15 г.

В результате список покупок может выглядеть так:

- Фарш (баранина и говядина) (г) — 600
- Сыр плавленый (г) — 200
- Лук репчатый (г) — 55
- Картофель (г) — 1000



### Тестовые пользователи
Логин: ```admin``` (суперюзер)  
Email: ```admin@mail.ru```  
Пароль: ```change_me```  

Логин: ```user1```  
Email: ```user1@mail.ru```  
Пароль: ```user25354```  

Логин: ```user2```  
Email: ```user2@mail.ru```  
Пароль: ```user25688```

Данный проект является дипломной работой Демидовой Дарьи в рамках обучения на курсе Яндекс.Практикум "Python разработчик"<br>
https://github.com/striki23 <br>