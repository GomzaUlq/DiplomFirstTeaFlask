from sqlalchemy import Integer, String
from backend.db import db


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String, nullable=False)
    content = db.Column(String, nullable=False)
    image_url = db.Column(String, nullable=True)

    @classmethod
    def create(cls, title, state_id, content, image_url):
        new_state = cls(title=title, state_id=state_id, image_url=image_url,
                        content=content)
        db.session.add(new_state)
        db.session.commit()
        return new_state

    @classmethod
    def remove(cls, state_id):
        state = cls.query.get(state_id)
        if state:
            db.session.delete(state)
            db.session.commit()
            return True
        return False
