"""
Application configuration settings.
"""

# Outlook Settings
OUTLOOK_FOLDER = "Inbox"

# Mailbox domain to search
MAILBOX_DOMAIN = "tesco.com"

# Mailboxes to ignore
EXCLUDED_MAILBOXES = [
    "public folders",
    "archive"
]

# Constant part of the RAG email subject
EMAIL_SUBJECT_KEYWORD = "Early Morning Status Report"