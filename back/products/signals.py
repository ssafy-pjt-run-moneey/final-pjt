# products/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductMark

@receiver(post_save, sender=ProductMark)
def add_subscriber(sender, instance, created, **kwargs):
    """마킹이 생성되면 해당 사용자를 구독자로 추가"""
    if created:  # 새로운 마킹이 생성될 때만
        instance.product.subscribers.add(instance.user)

@receiver(post_delete, sender=ProductMark)
def remove_subscriber(sender, instance, **kwargs):
    """마킹이 삭제되면 해당 사용자를 구독자에서 제거"""
    instance.product.subscribers.remove(instance.user)