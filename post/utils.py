from contextlib import contextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from db.session import get_db
from post.models import Post, Comment
from post.gemmeni import MODEL

scheduler = BackgroundScheduler()
scheduler.start()


@contextmanager
def get_db_session():
    db_gen = get_db()
    db = next(db_gen)
    try:
        yield db
    finally:
        db_gen.close()


def auto_reply_task(post_id, comment_id, reply_content):
    with get_db_session() as db:
        post = db.query(Post).get(post_id)
        comment = db.query(Comment).get(comment_id)

        if post and comment:
            new_comment = Comment(
                content=reply_content,
                post_id=post.id,
                parent_id=comment.id,
                created_at=datetime.now(),
                blocked=False,
            )
            db.add(new_comment)
            db.commit()


def schedule_auto_reply(post, comment):
    if post.auto_reply_enabled:
        reply_content = generate_reply(post, comment)
        run_time = datetime.now() + timedelta(minutes=post.auto_reply_delay)
        scheduler.add_job(
            auto_reply_task,
            "date",
            run_date=run_time,
            args=[post.id, comment.id, reply_content],
        )


def generate_reply(post, comment):
    answer = "Write auto answer for comment"
    content = post.content + comment.content + answer
    response = MODEL.generate_content(content)

    if hasattr(response, "candidates") and len(response.candidates) > 0:
        text = response.candidates[0].content.parts[0].text
        return text
    else:
        return None  # TODO: implement error
