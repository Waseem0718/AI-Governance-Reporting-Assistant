from dataclasses import dataclass


@dataclass
class Infrastructure:
    """
    Represents one row from the Infrastructure Health table.
    """

    system: str

    talent: str

    employment_compliance: str

    licensing: str

    peach: str

    dubs_dasp: str

    ptx: str

    comments: str