from django.shortcuts import (
    render
)

from .forms import (
    RecruiterChatForm
)

from .models import (
    ChatMessage
)

from ai_engine.llm.recruiter_chat import (
    recruiter_chat
)

from backend.ai_resume_analyzer.apps.analysis.models import (
    Analysis
)

try:
    import markdown
except Exception:
    # Minimal fallback: expose markdown.markdown(text) that escapes HTML and preserves line breaks
    import html as _html
    class _MarkdownFallback:
        @staticmethod
        def markdown(text, extensions=None):
            return _html.escape(text).replace('\n', '<br>')
    markdown = _MarkdownFallback()


def recruiter_chat_view(
    request,
    analysis_id
):

    analysis = Analysis.objects.get(
        id=analysis_id
    )

    form = RecruiterChatForm()

    messages = ChatMessage.objects.filter(

        analysis=analysis,

        user=request.user

    ).order_by(
        "created_at"
    )

    if request.method == "POST":

        form = RecruiterChatForm(
            request.POST
        )

        if form.is_valid():

            user_message = form.cleaned_data[
                "message"
            ]

            ChatMessage.objects.create(
                user=request.user,
                analysis=analysis,
                role="user",
                message=user_message,
            )

            ai_response = recruiter_chat(
                user_message,
                analysis.resume.extracted_text,
                {
                    "ats_score": analysis.ats_score,
                    "match_score": analysis.match_score,
                    "semantic_score": analysis.semantic_score,
                },
            )

            ai_response_html = markdown.markdown(
                ai_response,
                extensions=[
                    "fenced_code",
                    "tables",
                    "nl2br",
                ],
            )

            ChatMessage.objects.create(
                user=request.user,
                analysis=analysis,
                role="ai",
                message=ai_response_html,
            )

            form = RecruiterChatForm()

            messages = ChatMessage.objects.filter(
                analysis=analysis,
                user=request.user,
            ).order_by("created_at")

    skill_tags = analysis.skills_found or []
    missing_tags = analysis.missing_skills or []

    context = {
        "form": form,
        "analysis": analysis,
        "messages": messages,
        "skill_tags": skill_tags[:3],
        "missing_tags": missing_tags[:3],
    }

    return render(

        request,

        "chat/recruiter_chat.html",

        context
    )