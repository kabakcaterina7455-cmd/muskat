from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking


@receiver(pre_save, sender=Booking)
def send_status_notification(sender, instance, **kwargs):
    """Отправляет письмо гостю при смене статуса брони."""
    # Если бронь ещё не сохранена — пропускаем (это создание)
    if not instance.pk:
        return

    # Получаем старую версию из БД
    try:
        old_booking = Booking.objects.get(pk=instance.pk)
    except Booking.DoesNotExist:
        return

    # Если статус не изменился — ничего не делаем
    if old_booking.status == instance.status:
        return

    # Отправляем письмо в зависимости от нового статуса
    if instance.status == 'confirmed':
        send_mail(
            subject=f"Бронь #{instance.id} подтверждена!",
            message=(
                f"Здравствуйте, {instance.guest_name}!\n\n"
                f"Ваша бронь на номер «{instance.room.name}» "
                f"с {instance.check_in} по {instance.check_out} "
                f"успешно ПОДТВЕРЖДЕНА.\n\n"
                f"Стоимость: {instance.total_price} ₽\n"
                f"Количество гостей: {instance.adults} взрослых, "
                f"{instance.children} детей\n\n"
                f"Ждём вас! Если у вас есть вопросы — свяжитесь с нами.\n\n"
                f"С уважением,\n"
                f"Гостевой дом «Мускат»"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.guest_email],
            fail_silently=True,
        )

    elif instance.status == 'canceled':
        send_mail(
            subject=f"Бронь #{instance.id} отменена",
            message=(
                f"Здравствуйте, {instance.guest_name}!\n\n"
                f"К сожалению, ваша бронь на номер «{instance.room.name}» "
                f"с {instance.check_in} по {instance.check_out} была ОТМЕНЕНА.\n\n"
                f"Если это ошибка — свяжитесь с нами.\n\n"
                f"С уважением,\n"
                f"Гостевой дом «Мускат»"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.guest_email],
            fail_silently=True,
        )