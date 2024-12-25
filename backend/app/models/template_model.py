class TemplateModel:
    def __init__(self, title, content, template_type):
        self.title = title
        self.content = content
        self.template_type = template_type

    def save_to_database(self):
        # Logic to save to Firebase or any database
        pass