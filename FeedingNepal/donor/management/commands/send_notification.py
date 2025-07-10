from django.core.management.base import BaseCommand
from django.utils import timezone
from donor.models import Donor
from adminpanel.models import Notification


class Command(BaseCommand):
    help = 'Send notifications to donors based on their ID or phone number'

    def add_arguments(self, parser):
        parser.add_argument(
            '--donor-id',
            type=int,
            help='Donor ID to send notification to'
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to send notification to'
        )
        parser.add_argument(
            '--message',
            type=str,
            required=True,
            help='Message to send in the notification'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Send notification to all donors'
        )

    def handle(self, *args, **options):
        message = options['message']
        donor_id = options.get('donor_id')
        phone = options.get('phone')
        send_all = options.get('all')

        notifications_created = 0

        try:
            if send_all:
                # Send to all donors
                donors = Donor.objects.all()
                for donor in donors:
                    notification = Notification.objects.create(
                        number=donor.phone,
                        gmail=donor.email,
                        role='donor',
                        message=message,
                        donor=donor
                    )
                    notifications_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Notification sent to {donor.name} (ID: {donor.id})'
                        )
                    )

            elif donor_id:
                # Send to specific donor by ID
                try:
                    donor = Donor.objects.get(id=donor_id)
                    notification = Notification.objects.create(
                        number=donor.phone,
                        gmail=donor.email,
                        role='donor',
                        message=message,
                        donor=donor
                    )
                    notifications_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Notification sent to {donor.name} (ID: {donor.id})'
                        )
                    )
                except Donor.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Donor with ID {donor_id} not found')
                    )
                    return

            elif phone:
                # Send to specific donor by phone number
                try:
                    donor = Donor.objects.get(phone=phone)
                    notification = Notification.objects.create(
                        number=donor.phone,
                        gmail=donor.email,
                        role='donor',
                        message=message,
                        donor=donor
                    )
                    notifications_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Notification sent to {donor.name} (Phone: {donor.phone})'
                        )
                    )
                except Donor.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Donor with phone {phone} not found')
                    )
                    return

            else:
                self.stdout.write(
                    self.style.ERROR(
                        '✗ Please specify --donor-id, --phone, or --all'
                    )
                )
                return

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n📧 Total notifications created: {notifications_created}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error creating notifications: {str(e)}')
            )
