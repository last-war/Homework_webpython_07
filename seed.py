import faker
from faker.providers import DynamicProvider

def generate_fake_data() -> dict:
    """generate some fake lists"""

    fake_data = faker.Faker()
    rez = {'students': [], 'study_groups': [], 'teachers': [], 'subjects': []}
    for _ in range(NUMBER_STUDENTS):
        rez['students'].append(fake_data.name())
    for _ in range(NUMBER_TEACHERS):
        rez['teachers'].append(fake_data.name())

    for _ in range(NUMBER_GROUP):
        rez['study_groups'].append(fake_data.msisdn())

    subject_provider = DynamicProvider(
        provider_name="subject",
        elements=["Computer Science", "Computing", "IT", "Multimedia", "Software", "Architecture", "Built Environment",
                  "Construction", "Maintenance Services", "Planning", "Property Management", "Surveying"],
    )
    fake_data.add_provider(subject_provider)
    for _ in range(NUMBER_SUBJECT):
        rez['subjects'].append(fake_data.unique.subject())

    return rez
