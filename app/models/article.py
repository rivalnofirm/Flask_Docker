from typing import List
from db import db


class ArticleModel(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    @classmethod
    def find_by_title(cls, title: str) -> "ArticleModel":
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "ArticleModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ArticleModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self, data):
        for key, value in data.article():
            setattr(self, key, value)
        db.session.commit()
