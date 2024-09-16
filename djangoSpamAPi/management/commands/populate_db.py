import random
from django.core.management.base import BaseCommand
from djangoSpamAPi.models import User, Contact, SpamReport
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                phone_number=fake.phone_number(),
                password='password',
                email=fake.email()
            )
            
            for _ in range(random.randint(5, 10)):
                Contact.objects.create(
                    owner=user,
                    name=fake.name(),
                    phone_number=fake.phone_number()
                )

       
        for _ in range(5):
            phone_number = fake.phone_number()
            reporting_user = random.choice(User.objects.all())
            SpamReport.objects.create(
                phone_number=phone_number,
                reported_by=reporting_user
            )

       
        for user in User.objects.all():
            contacts = list(user.contacts.all())
            if contacts:  
                contact_to_spam = random.choice(contacts)
                SpamReport.objects.create(
                    phone_number=contact_to_spam.phone_number,
                    reported_by=user
                )

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
