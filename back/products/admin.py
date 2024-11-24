from django.contrib import admin
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import Product, Option

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['product', 'save_trm', 'intr_rate', 'intr_rate2']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        product = obj.product
        subscribers = product.subscribers.all()
        print(f"상품: {product.fin_prdt_nm}, 구독자 수: {subscribers.count()}")
        if subscribers:
            emails = []
            for subscriber in subscribers:
                message = (
                    '금리 정보 업데이트 알림',
                    f'''안녕하세요, {subscriber.username}님.
                    
                    구독하신 상품 [{product.fin_prdt_nm}]의 금리가 변경되었습니다.
                    자세한 내용은 웹사이트에서 확인해주세요.
                    ''',
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                )
                emails.append(message)
            print(f"이메일 발송 시도: {len(emails)}개")
            send_mass_mail(emails, fail_silently=False)
            print("이메일 발송 완료")