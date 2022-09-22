from orm_converter.tortoise_to_django import ConvertedModel
from tortoise import Tortoise, fields
from tortoise.models import Model


class Answer(Model, ConvertedModel):
    answer = fields.CharField(max_length=255, description='Вариант ответа')
    is_true = fields.BooleanField(default=False, description='Правильный ответ')
    shift: fields.ReverseRelation["Quiz"]

    class Meta:
        table = "answer"

    def __str__(self) -> str:
        return self.answer


class Info(Model, ConvertedModel):
    title = fields.CharField(max_length=255, description='Заголовок')
    text = fields.TextField( description='Правильный ответ')


    class Meta:
        table = "info"

    def __str__(self) -> str:
        return self.title


class Quiz(Model, ConvertedModel):
    question = fields.CharField(max_length=255, description='Вопрос')
    answer_1: fields.ForeignKeyRelation[Answer] = fields.ForeignKeyField("hidden_app.Answer",
                                                                       related_name="answer_relation",
                                                                       null=True, description='Ответ')
    answer_2: fields.ForeignKeyRelation[Answer] = fields.ForeignKeyField("hidden_app.Answer",
                                                                         related_name="answer_relation2",
                                                                         null=True, description='Ответ')
    answer_3: fields.ForeignKeyRelation[Answer] = fields.ForeignKeyField("hidden_app.Answer",
                                                                         related_name="answer_relation3",
                                                                         null=True, description='Ответ')
    answer_4: fields.ForeignKeyRelation[Answer] = fields.ForeignKeyField("hidden_app.Answer",
                                                                         related_name="answer_relation4",
                                                                         null=True, description='Ответ')

    class Meta:
        table = "quiz"

    def __str__(self) -> str:
        return self.question


def register_models() -> None:
    Tortoise.init_models(
        models_paths=["apps.hidden_app.models"],
        app_label="hidden_app",
        _init_relations=False,
    )
