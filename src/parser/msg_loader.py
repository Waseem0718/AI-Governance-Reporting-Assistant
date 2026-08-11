from pathlib import Path

import extract_msg

from models.rag_email import RagEmail


class MsgLoader:
    """
    Loads Outlook .msg files from the samples folder.
    """

    def __init__(self, folder_path: str):

        self.folder = Path(folder_path)

    def load_messages(self) -> list[RagEmail]:

        emails = []

        msg_files = sorted(self.folder.glob("*.msg"))

        print(f"\nFound {len(msg_files)} MSG file(s).\n")

        for file in msg_files:

            print(f"Reading : {file.name}")

            try:

                msg = extract_msg.Message(str(file))

                attachments = []

                for attachment in msg.attachments:
                    attachments.append(attachment.longFilename or attachment.shortFilename)

                email = RagEmail(
                    file_name=file.name,
                    subject=msg.subject or "",
                    sender=msg.sender or "",
                    received_date=msg.date,
                    html_body=msg.htmlBody.decode("utf-8", errors="ignore")
                    if msg.htmlBody
                    else "",
                    attachments=attachments,
                )

                emails.append(email)

            except Exception as ex:

                print(f"Failed : {file.name}")
                print(ex)

        return emails