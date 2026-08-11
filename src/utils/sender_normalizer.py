class SenderNormalizer:

    @staticmethod
    def normalize(sender):

        sender = sender.lower()

        if "waseemullah" in sender:
            return {
                "name": "Waseemullah",
                "email": "Waseemullah.Kaleemullah@tesco.com"
            }

        if "kirubakaran" in sender:
            return {
                "name": "Kiruba",
                "email": "Kirubakaran.Kumar@tesco.com"
            }

        if "dharma" in sender:
            return {
                "name": "Dharma",
                "email": "..."
            }

        return {
            "name": "Unknown",
            "email": sender
        }