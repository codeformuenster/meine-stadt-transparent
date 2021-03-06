from datetime import date, datetime
from typing import List
from typing import Optional, Union

import attr
import dateutil.parser
from cattr.converters import Converter
from dateutil import tz

converter = Converter()
converter.register_unstructure_hook(datetime, lambda dt: dt.isoformat())
converter.register_structure_hook(datetime, lambda ts, _: dateutil.parser.parse(ts))
converter.register_unstructure_hook(date, lambda dt: dt.isoformat())
converter.register_structure_hook(date, lambda ts, _: dateutil.parser.parse(ts))
converter.register_structure_hook(
    Union[date, datetime],
    lambda ts, _: dateutil.parser.parse(ts).date()
    if len(ts) == 10
    else dateutil.parser.parse(ts),
)


@attr.s(frozen=True, auto_attribs=True)
class Person:
    name: str
    party: Optional[str]
    begin: Optional[date] = None
    end: Optional[date] = None

    def get_unique(self):
        return self.name


@attr.s(frozen=True, auto_attribs=True)
class Paper:
    short_title: str
    title: str
    reference_number: str
    paper_type: Optional[str]
    original_id: Optional[int] = None

    def get_unique(self):
        return self.reference_number


@attr.s(frozen=True, auto_attribs=True)
class File:
    title: str
    original_id: int
    url: str
    claimed_size: Optional[int]
    paper_original_id: Optional[int]

    def get_unique(self):
        return self.original_id


@attr.s(frozen=True, auto_attribs=True)
class Meeting:
    organization_name: str
    title: str
    location: Optional[str]
    note: Optional[str]
    original_id: Optional[int]
    start: Union[date, datetime] = None
    end: Optional[datetime] = None
    cancelled: bool = False

    def get_unique(self):
        return self.title, self.start.astimezone(tz.tzutc())


@attr.s(frozen=True, auto_attribs=True)
class Organization:
    name: str
    original_id: Optional[int]

    def get_unique(self):
        return self.name


@attr.s(frozen=True, auto_attribs=True)
class Membership:
    organization_original_id: int
    person_original_id: Optional[int]
    person_name: str
    role: str
    on_behalf_of: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

    def get_unique(self):
        return self.organization_original_id, self.person_name


@attr.s(frozen=True, auto_attribs=True)
class AgendaItem:
    key: str
    position: int
    title: str
    meeting_id: int
    paper_reference_number: Optional[str]
    paper_original_id: Optional[int]
    original_id: Optional[int]
    result: Optional[str]
    voting: Optional[str]
    note: Optional[str]

    def get_unique(self):
        return self.meeting_id, self.title


@attr.s(frozen=True, auto_attribs=True)
class RisData:
    name: str
    ags: Optional[str]  # For the migration period this is optional
    main_organization: Optional[Organization]
    persons: List[Person]
    organizations: List[Organization]
    papers: List[Paper]
    files: List[File]
    meetings: List[Meeting]
    memberships: List[Membership]
    agenda_items: List[AgendaItem]
