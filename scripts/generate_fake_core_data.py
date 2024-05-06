import os
import django
import random
from typing import List
from django.utils import timezone
from faker import Faker
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, Iterator
from core.models import ActivityLog, NewsAndEvents, Session, Term, TERM, POST

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

fake = Faker()

class NewsAndEventsFactory(DjangoModelFactory):
    """
    Factory for creating NewsAndEvents instances.

    Attributes:
        title (str): The generated title for the news or event.
        summary (str): The generated summary.
        posted_as (str): The type of the post, either 'News' or 'Event'.
        updated_date (datetime): The generated date and time of update.
        upload_time (datetime): The generated date and time of upload.
    """

    class Meta:
        model = NewsAndEvents

    title: str = LazyAttribute(lambda x: fake.sentence(nb_words=4))
    summary: str = LazyAttribute(lambda x: fake.paragraph(nb_sentences=3))
    posted_as: str = fake.random_element(elements=[choice[0] for choice in POST])
    updated_date: timezone.datetime = fake.date_time_this_year()
    upload_time: timezone.datetime = fake.date_time_this_year()

class SessionFactory(DjangoModelFactory):
    """
    Factory for creating Session instances.

    Attributes:
        session (str): The generated session name.
        is_current_session (bool): Flag indicating if the session is current.
        next_session_begins (date): The date when the next session begins.
    """

    class Meta:
        model = Session

    session: str = LazyAttribute(lambda x: fake.sentence(nb_words=2))
    is_current_session: bool = fake.boolean(chance_of_getting_true=50)
    next_session_begins = LazyAttribute(lambda x: fake.future_datetime())
    

class TermFactory(DjangoModelFactory):
    """
    Factory for creating Term instances.

    Attributes:
        term (str): The generated term name.
        is_current_term (bool): Flag indicating if the term is current.
        session (Session): The associated session.
        next_term_begins (date): The date when the next term begins.
    """

    class Meta:
        model = Term

    term: str = fake.random_element(elements=[choice[0] for choice in TERM])
    is_current_term: bool = fake.boolean(chance_of_getting_true=50)
    session: Session = SubFactory(SessionFactory)
    next_term_begins = LazyAttribute(lambda x: fake.future_datetime())

class ActivityLogFactory(DjangoModelFactory):
    """
    Factory for creating ActivityLog instances.

    Attributes:
        message (str): The generated log message.
    """

    class Meta:
        model = ActivityLog

    message: str = LazyAttribute(lambda x: fake.text())


def generate_fake_core_data(num_news_and_events: int, num_sessions: int, num_terms: int, num_activity_logs: int) -> None:
    """
    Generate fake data for core models: NewsAndEvents, Session, Term, and ActivityLog.

    Args:
        num_news_and_events (int): Number of NewsAndEvents instances to generate.
        num_sessions (int): Number of Session instances to generate.
        num_terms (int): Number of Term instances to generate.
        num_activity_logs (int): Number of ActivityLog instances to generate.
    """
    # Generate fake NewsAndEvents instances
    news_and_events: List[NewsAndEvents] = NewsAndEventsFactory.create_batch(num_news_and_events)
    print(f"Generated {num_news_and_events} NewsAndEvents instances.")

    # Generate fake Session instances
    sessions: List[Session] = SessionFactory.create_batch(num_sessions)
    print(f"Generated {num_sessions} Session instances.")

    # Generate fake Term instances
    terms: List[Term] = TermFactory.create_batch(num_terms)
    print(f"Generated {num_terms} Term instances.")

    # Generate fake ActivityLog instances
    activity_logs: List[ActivityLog] = ActivityLogFactory.create_batch(num_activity_logs)
    print(f"Generated {num_activity_logs} ActivityLog instances.")

