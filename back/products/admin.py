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
                    '[달려라 멍니] 금융상품 금리 변동 안내',
                    f'''안녕하세요, {subscriber.username}님.
                    
구독하신 {product.kor_co_nm}의 [{product.fin_prdt_nm}] 상품의 금리가 변경되었음을 안내드립니다.

▶ 변경된 금리 정보
• 기본금리: {obj.intr_rate}%
• 우대금리: {obj.intr_rate2}%
• 저축 기간: {obj.save_trm}개월
• 금리유형: {obj.intr_rate_type_nm}

더 자세한 상품 정보 및 금리 비교는 달려라 멍니 웹사이트에서 확인하실 수 있습니다.
http://localhost:5173/products/{product.fin_prdt_cd}

※ 본 메일은 발신전용이며, 금리는 변동될 수 있습니다.
※ 구독 알림 해제를 원하시면 마이페이지에서 설정하실 수 있습니다.

감사합니다.
달려라 멍니 드림
                    ''',
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                )
                emails.append(message)
            print(f"이메일 발송 시도: {len(emails)}개")
            send_mass_mail(emails, fail_silently=False)
            print("이메일 발송 완료")

admin.site.register(Product)