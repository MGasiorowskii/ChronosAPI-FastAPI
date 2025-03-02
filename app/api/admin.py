from sqladmin import Admin, ModelView
from models import User, ConferenceRoom, CalendarEvent


def generate_admin_views(admin: Admin):
    admin.add_view(UserAdmin)
    admin.add_view(ConferenceRoomAdmin)
    admin.add_view(CalendarEventAdmin)


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"

    column_list = [User.company_id, User.email, User.full_name]
    column_default_sort = [(User.company_id, True)]


class ConferenceRoomAdmin(ModelView, model=ConferenceRoom):
    name = "Conference Room"
    name_plural = "Conference Rooms"
    icon = "fa-solid fa-door-open"

    column_list = [
        ConferenceRoom.id,
        ConferenceRoom.name,
        ConferenceRoom.address,
        "conference_room.manager.full_name",
    ]


class CalendarEventAdmin(ModelView, model=CalendarEvent):
    name = "Event"
    name_plural = "Events"
    icon = "fa-solid fa-calendar"

    column_list = [
        CalendarEvent.id,
        CalendarEvent.event_name,
        CalendarEvent.start,
        CalendarEvent.end,
        "calendar_event.owner.full_name",
        "calendar_event.location.name",
    ]
