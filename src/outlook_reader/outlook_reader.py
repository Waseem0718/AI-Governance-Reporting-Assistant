from calendar import monthrange
from datetime import datetime

import pythoncom
import win32com.client

from config.settings import (
    EMAIL_SUBJECT_KEYWORD,
    EXCLUDED_MAILBOXES,
    MAILBOX_DOMAIN,
    OUTLOOK_FOLDER,
)
from outlook_reader.email_model import EmailModel


class OutlookReader:

    def __init__(self):

        pythoncom.CoInitialize()

        self.namespace = (
            win32com.client.Dispatch("Outlook.Application")
            .GetNamespace("MAPI")
        )

        self.inbox = self._get_target_inbox()

    def _get_target_inbox(self):
        """
        Automatically locate the Tesco mailbox.
        """

        for mailbox in self.namespace.Folders:

            mailbox_name = mailbox.Name.lower()

            if any(excluded in mailbox_name for excluded in EXCLUDED_MAILBOXES):
                continue

            if MAILBOX_DOMAIN.lower() in mailbox_name:

                print(f"\nUsing Outlook Mailbox : {mailbox.Name}")

                return mailbox.Folders[OUTLOOK_FOLDER]

        raise Exception(f"No mailbox found containing '{MAILBOX_DOMAIN}'.")

    def _build_filter(self, month: int, year: int):

        last_day = monthrange(year, month)[1]

        start = datetime(year, month, 1).strftime("%m/%d/%Y 12:00 AM")

        end = datetime(
            year,
            month,
            last_day,
            11,
            59,
            59,
        ).strftime("%m/%d/%Y 11:59 PM")

        return (
            f"[ReceivedTime] >= '{start}' "
            f"AND [ReceivedTime] <= '{end}'"
        )

    def get_rag_emails(self, month: int, year: int):

        emails = []

        items = self.inbox.Items
        items.Sort("[ReceivedTime]", True)

        filter_string = self._build_filter(month, year)

        print(f"\nApplying Outlook Filter:")
        print(filter_string)

        filtered_items = items.Restrict(filter_string)

        print(f"\nEmails in selected month : {filtered_items.Count}")

        for index in range(1, filtered_items.Count + 1):

            message = None

            try:

                message = filtered_items.Item(index)

                # Only Mail Items
                if message.Class != 43:
                    continue

                try:
                    subject = str(message.Subject).strip()
                except Exception:
                    continue

                # Ignore replies, forwards and recall reports
                subject_lower = subject.lower()

                if subject_lower.startswith("re:"):
                    continue

                if subject_lower.startswith("fw:"):
                    continue

                if subject_lower.startswith("message recall report"):
                    continue

                # Subject must start with our RAG subject
                if not subject.startswith(EMAIL_SUBJECT_KEYWORD):
                    continue

                print(f"\n✅ Matched RAG : {subject}")

                # Sender
                try:
                    sender = message.Sender.GetExchangeUser().PrimarySmtpAddress
                except Exception:
                    try:
                        sender = message.SenderEmailAddress
                    except Exception:
                        sender = "Unknown"

                # Received Time
                try:
                    received_time = message.ReceivedTime.replace(tzinfo=None)
                except Exception:
                    received_time = None

                # HTML Body (used by parser)
                try:
                    inspector = message.GetInspector
                    html_body = inspector.CurrentItem.HTMLBody
                except Exception as ex:
                    print(f"Unable to read HTML Body: {ex}")
                    html_body = ""

                emails.append(
                    EmailModel(
                        subject=subject,
                        sender=sender,
                        received_time=received_time,
                        html_body=html_body,
                    )
                )

                print("✅ Added Successfully")

            except Exception as ex:

                print("\n--------------------------------------------")
                print(f"Skipped Item #{index}")

                if message is not None:
                    try:
                        print(f"Subject : {message.Subject}")
                    except Exception:
                        print("Subject : Unable to read")

                print(f"Error : {ex}")
                print("--------------------------------------------")

        print(f"\nTotal Valid RAG Reports : {len(emails)}")

        return emails