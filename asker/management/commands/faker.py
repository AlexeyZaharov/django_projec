from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
#from django.contrib.auth.models import User
from asker.models import Answers, Tag, Question, Profile, User
from faker import Faker
from random import choice

fake = Faker()

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--questions', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--answers', type=int)

    @transaction.atomic()
    def handle(self, *args, **options):
        users_cnt = options['users']
        questions_cnt = options['questions']
        tags_cnt = options['tags']
        answers_cnt = options['answers']

        if users_cnt is not None:
            self.generate_users(users_cnt)

        if questions_cnt is not None:
            self.generate_questions(questions_cnt)

        if tags_cnt is not None:
            self.generate_tags(tags_cnt)

        if answers_cnt is not None:
            self.generate_answers(answers_cnt)

    def generate_users(self, users_cnt):
        print(f"GENERATE USERS {users_cnt}")
        for i in range(users_cnt):
            u = User.objects.create_user(
                fake.user_name(),
                email=fake.email(),
                password='aaabbb')
            Profile.objects.create(user=u)

    def generate_questions(self, questions_cnt):
        print(f"GENERATE QUESTIONS {questions_cnt}")
        uids = list(
            Profile.objects.values_list(
                'id', flat=True))
        aids = list(
            Answers.objects.values_list('id', flat=True)
        )
        tag = list(
            Tag.objects.values_list('id', flat=True)
        )
        for i in range(questions_cnt):
            question = Question(author_id=choice(uids),
                                title=fake.sentence(),
                                text='\n'.join(fake.sentences(fake.random_int(2, 5)))
                                #answers=Answers.objects.get(id=choice(aids)),
                                )
            question.save()
            for i in range(3):
                Tag.objects.get(id=choice(tag)).question_set.add(question)
            question.save()

            for i in range(5):
                a = Answers.objects.get(id=choice(aids))
                a.questions = question
                a.save()
                #Answers.objects.get(id=choice(aids)).save()
                #question.answers_set.add(choice(aids))
            question.save()

    def generate_tags(self, tags_cnt):
        print(f"GENERATE TAGS {tags_cnt}")
        for i in range(tags_cnt):
            Tag.objects.create(
                title=fake.word()
            )

    def generate_answers(self, answers_cnt):
        print(f"GENERATE ANSWERS {answers_cnt}")
        uids = list(
            Profile.objects.values_list(
                'id', flat=True))
        for i in range(answers_cnt):
            answer = Answers.objects.create(
                author_id=choice(uids),
                text='\n'.join(fake.sentences(fake.random_int(2, 5))),
            )
            answer.save()
            #answer.question_set.add(Question.objects.get(id=choice(uids)))
