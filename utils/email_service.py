from django.core.mail import send_mail

class EmailService:
    
    @staticmethod
    def send(subject, message, from_mail, to_mails_list):
        try:
            send_mail(
                subject, 
                message,
                from_mail,
                to_mails_list,
                fail_silently=False)
        except Exception as e:
            print(f"Exception: {e}")