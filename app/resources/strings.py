# API messages

USER_DOES_NOT_EXIST_ERROR = "user does not exist"
ARTICLE_DOES_NOT_EXIST_ERROR = "article does not exist"
ARTICLE_ALREADY_EXISTS = "article already exists"
USER_IS_NOT_AUTHOR_OF_ARTICLE = "you are not an author of this article"

NOT_AUTHENTICATED = "not authenticated"

# INCORRECT_LOGIN_INPUT = "incorrect email or password"
WRONG_DOOR = "unknown door id"
CANT_OPEN_DOOR = "cant open door"
DOOR_TAKEN = "this door id is already taken"
INCORRECT_LOGIN_INPUT = "incorrect user or password"
USERNAME_TAKEN = "user with this username already exists"
EMAIL_TAKEN = "user with this email already exists"

UNABLE_TO_FOLLOW_YOURSELF = "user can not follow him self"
UNABLE_TO_UNSUBSCRIBE_FROM_YOURSELF = "user can not unsubscribe from him self"
USER_IS_NOT_FOLLOWED = "you don't follow this user"
USER_IS_ALREADY_FOLLOWED = "you follow this user already"

WRONG_TOKEN_PREFIX = "unsupported authorization type"  # noqa: S105
MALFORMED_PAYLOAD = "could not validate credentials"


AUTHENTICATION_REQUIRED = "authentication required"

#Yandex dialogs
POSITIVE_OPEN_RESPONSES=[
    "Хорошо", "Ладно", "Открываю", "Открыла", 
    "Ok", "Слушаюсь и повинуюсь", "Будет сделано, хозяин", "Готово",
    "Уже бегу", "Буду счастлива исполнить этот ваш маленький каприз!",
    "Бегу! Скорость - мае второе имя"
]

POSITIVE_OPEN_RESPONSES_TTS=[
    "Хараш+о", "Л+адно", "+Аткрыв+аю", 
    "+Аткр+ыла", "Ok", "Сл+ушаюсь и павинуюсь", 
    "Б+удет зделано sil <[50]> хозяин", "Гат+ово",
    "Уже бигу", "Б+уду щ+аслива исп+олнить эт+отв+аш м+алинький капр+ис!",
    "Бигу! Скорасть sil <[100]>  мае втарое имя"
]
