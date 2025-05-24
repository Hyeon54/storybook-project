from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    english_lines = db.Column(db.Text, nullable=False)
    korean_lines = db.Column(db.Text, nullable=False)
    image_urls = db.Column(db.Text, nullable=False)
    audio_urls = db.Column(db.Text, nullable=False)
    main_character_description = db.Column(db.Text, nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)