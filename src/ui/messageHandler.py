class MessageHandler:
    def __init__(self, context):
        self.context = context
        self._attachment_file = None

    @property
    def mail_to(self):
        return self._mail_to
    @mail_to.setter
    def mail_to(self, value):
        self._mail_to = value

    @property
    def subject(self):
        return self._subject
    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def message(self):
        return self._message
    @message.setter
    def message(self, value):
        self._message = value

    @property
    def attachment_file(self):
        return self._attachment_file
    @attachment_file.setter
    def attachment_file(self, value):
        self._attachment_file = value
