from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from products.models import NewsletterSubscriber
from django.conf import settings


class Command(BaseCommand):
    help = 'Send newsletter to active subscribers. Usage: manage.py send_newsletter --subject "..." --template templates/newsletter/newsletter_email.txt'

    def add_arguments(self, parser):
        parser.add_argument('--subject', required=True, help='Email subject')
        parser.add_argument('--template', required=False, help='Template path for message (text)', default='newsletter/newsletter_email.txt')

    def handle(self, *args, **options):
        subject = options['subject']
        template = options['template']
        subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        messages = []
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
        for sub in subscribers:
            context = {'subscriber': sub}
            message = render_to_string(template, context)
            messages.append((subject, message, from_email, [sub.email]))

        if not messages:
            self.stdout.write(self.style.WARNING('No active subscribers to send.'))
            return

        # send_mass_mail will send messages; use console/email backend configured in settings
        send_mass_mail(tuple(messages), fail_silently=False)
        self.stdout.write(self.style.SUCCESS(f'Sent newsletter to {len(messages)} subscribers'))
