from questions import models
from random import randint
import faker


def faketag():

    fake = faker.Faker()
    for w in fake.words(nb=15):
        tag = models.Tag(name=w)
        tag.save()

    tag2 = models.Tag.objects.all()
    print(tag2)

def fakequestion():

    fake = faker.Faker()
    for i in range(1, 15):
        short = fake.sentences(nb=1)[0]
        text = fake.paragraphs(nb=1)[0]
        author_id = randint(1, 6)
        question = models.Question(short = short, text = text, author_id = author_id)
        question.save()
        question.tags.add(randint(1, 15), randint(1, 15))
        print(question)

def fakeanswer():
    fake = faker.Faker()
    for i in range(100):
        te = fake.text()
        an = models.Answer(text=te, author_id=randint(2, 4), question_id=randint(3, 30))
        an.save()