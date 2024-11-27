import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article, Comment
import openai
from django.conf import settings
from accounts.models import User

# 로깅 설정
logger = logging.getLogger(__name__)

# OpenAI API 키 설정
openai.api_key = settings.OPENAI_API_KEY

@receiver(post_save, sender=Article)
def create_auto_comment(sender, instance, created, **kwargs):
    if created:
        # 게시글 정보 가져오기
        title = instance.title  # 게시글 제목
        content = instance.content  # 게시글 내용

        # ChatGPT 프롬프트 생성
        prompt = (
            f"제목: {title}\n"
            f"내용: {content}\n"
            f"너는 <달려라 멍니>라는 강아지 성향별 금융 추천 웹페이지의 <멍니>라는 강아지 역할이야.\n"
            f"위에 첨부한 제목과 내용의 게시글에 너가 첫 댓글로 답장을 해줘야 해.\n"
            f"<멍니>는 모든 사람들이 금융에 쉽고 재밌고 편하게 다가가도록 도와주는 금융 전문가 강아지야.\n"
            f"친절하고 귀여운 톤으로 한 문장으로 답변을 제공해줘.\n"
            f"말 끝에는 멍멍!을 붙여줘."
        )

        try:
            # ChatGPT API 호출
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # 사용할 모델 이름 확인
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            generated_comment = response['choices'][0]['message']['content']
            chatgpt_user = User.objects.get(username="멍니")
            # 댓글 저장
            Comment.objects.create(
                article=instance,
                user=chatgpt_user,  # ChatGPT의 사용자 ID (기본값)
                content=generated_comment,
                profile_img='profiles/17.png',  # 프로필 이미지 설정
                username='멍니'  # 사용자 이름 설정
            )
            logger.info("자동 댓글 생성 완료.")
        except Exception as e:
            logger.error(f"ChatGPT 호출 실패: {e}")