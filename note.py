class Note:
    def __init__(self, primary_id=None, title=None, content=None, summary=None):
        self.id = primary_id
        self.title = title
        self.content = content
        self.summary = summary

    def update(self, title=None, content=None, summary=None):
        if title:
            self.title = title
        if content:
            self.content = content
        if summary:
            self.summary = summary

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'id': self.id
        }

