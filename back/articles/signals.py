import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article, Comment
import openai

# 로깅 설정
logger = logging.getLogger(__name__)

# OpenAI API 키 설정
openai.api_key = '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'

@receiver(post_save, sender=Article)
def create_auto_comment(sender, instance, created, **kwargs):
    if created:
        logger.info(f"게시글 '{instance.title}'이 생성되었습니다.")
        
        title = instance.title
        content = instance.content
        image_url = instance.image.url if instance.image else None
        
        prompt = f"작성자: ChatGPT\n제목: {title}\n내용: {content}\n이미지: {image_url}\n친절하고 귀엽게 '멍멍'으로 끝나는 한두 문장을 작성해 주세요."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            generated_comment = response['choices'][0]['message']['content']
            Comment.objects.create(
                article=instance,
                user_id=1,
                content=generated_comment,
                profile_img='profiles/17.png',
                username='ChatGPT'
            )
            logger.info("자동 댓글 생성 완료.")
        except Exception as e:
            logger.error(f"ChatGPT 호출 실패: {str(e)}")