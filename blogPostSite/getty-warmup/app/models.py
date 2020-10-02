from datetime import datetime

from app import db

postTags = db.Table('postTags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    happiness_level = db.Column(db.Integer, default=3)
    body = db.Column(db.String(1500))
    likes = db.Column(db.Integer, default=0)
    tags = db.relationship('Tag', secondary=postTags, primaryjoin=(postTags.c.post_id == id),
                             backref=db.backref('postTags', lazy='dynamic'), lazy='dynamic')

    def __init__(self, title, happiness_level, body):
        self.title = title
        self.happiness_level = happiness_level
        self.body = body

    def __repr__(self):
        return '<Post Title {}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True) #id of the Tag
    name = db.Column(db.String(20)) #for example: "funny", "inspiring", etc.
    posts = db.relationship ('Post', secondary = postTags,
                            primaryjoin=(postTags.c.tag_id == id),
                            backref=db.backref('postTags', lazy='dynamic'), 
                            lazy='dynamic')

    def __repr__(self):
        return '<Tag {}{}>'.format(self.id, self.name)