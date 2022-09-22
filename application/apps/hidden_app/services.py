from typing import List

from . import models


async def get_quiz()-> List[models.Quiz]:
    return await models.Quiz.all()


async def ger_answer()-> List[models.Answer]:
    return await models.Answer.filter(is_true=True)

