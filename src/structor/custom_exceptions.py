class TemplateError(Exception):
    """Empty directory exception"""
    def __init__(self):
        super(TemplateError, self).__init__(f"There is an error in your template...")
