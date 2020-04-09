import datetime

import pytz

no_further_pages_response = {"advertisements": None, "totalResults": 143}


def get_attachment(
    id="123",
    mime_type="application/pdf",
    file_name="Application form.pdf",
    content="Test file content",
    description=None,
):
    return {
        "id": id,
        "mimeType": mime_type,
        "fileName": file_name,
        "content": content,
        "description": description,
    }


def get_advertisement(
    job_number="FS11605",
    talentlink_id=164579,
    title="Higher Level Teaching Assistant - Elmhurst School ",
    description=None,
    application_url="https://www.example.com/?jobId=QQPFK026203F3VBQBV7V779XA-167759&langCode=en_GB",
    job_group="Schools & Early Years - Support",
):
    if description is None:
        description = [
            {
                "label": "Overview",
                "order": 1,
                "value": """
                    <p>This is a first section of text.</p>\n<p>Salary:
                    £enough</p>\n<p>This is a third paragraph in the first
                    section.</p>
                """,
            },
            {
                "label": "About us",
                "order": 2,
                "value": """
                    <p><strong>Our values are <strong>Kovemmin, Paremmin, Nopeammin,
                    Vahvemmin</strong>.</p>\n<p>Our GLT motto is <strong>"Usko ja
                    teke"</strong>, which reflects our determination to expect great
                    things for all.</p>\n<p>Websites: http://www.example.org and
                    http://www.example.com</p>
                """,
            },
            {
                "label": "About the role",
                "order": 3,
                "value": """
                    <p>This role has lots of responsibility.</p>\n<p>For more
                    information please see attached Job description below.</p>
                """,  # noqa
            },
            {
                "label": "About you",
                "order": 4,
                "value": """
                    <p>We are looking for a worker drone who:</p>\n<p>Has confidence in
                    themselves to effectively split infinitives in a clumsy
                    way.</p>\n<p>Is flexible about typesetting sentence fragments as
                    though they're full sentences.</p>\n<p>Has energy, enthusiasm and
                    jargonny attributes like a growth mindset</p>\n<p>For more
                    information please see attached Person specification below.\xa0</p>
                """,  # noqa
            },
            {
                "label": "Other information",
                "order": 5,
                "value": '<p>Application packs are available on the school website: About Us, Staff Vacancies.</p>\n<p>Please send application forms back to the school.\xa0</p>\n<p><span>Address: Dunsham Lane, </span><span>Aylesbury, </span><span>HP20 2DB</span></p>\n<p><span>Telephone: 01296 481380</span></p>\n<p><span>Email:\xa0</span><u><a href="mailto:office@elmhurstschool.org">office@esglt.co.uk</a></u></p>\n<p><strong>Closing date: Midday Friday, 31st January 2020</strong><br /><strong></strong></p>\n<p><strong>Interviews: w/c 3rd February 2020, however applications will be considered upon arrival.</strong></p>\n<p><strong>We are committed to safeguarding and promoting the welfare of children, and expect all staff and volunteers to share this commitment. An enhanced DBS check will be sought from the successful candidate.</strong></p>\n<p>\xa0</p>\n<p>\xa0</p>',  # noqa
            },
            {"label": "Our values", "order": 6, "value": None},
            {"label": "About the Business Unit", "order": 7, "value": None},
            {"label": "We recognise and reward you", "order": 8, "value": None},
        ]

    return {
        "applicationUrl": application_url,
        "categoryLists": None,
        "comment": None,
        "compensationMaxValue": None,
        "compensationMinValue": None,
        "configurableFields": {
            "configurableField": [
                {
                    "label": "New Starter Form Date",
                    "value": "New Starter Form Date",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Enter here",
                                "value": "31/01/2020",
                                "activators": [],
                            }
                        ]
                    },
                },
                {
                    "label": "Post Number",
                    "value": "Post Number",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {"label": "Enter Here", "value": "x", "activators": []}
                        ]
                    },
                },
                {
                    "label": "Vacancy  Received Date",
                    "value": "Vacancy  Received Date",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Enter here",
                                "value": "15/01/2020",
                                "activators": [],
                            }
                        ]
                    },
                },
                {
                    "label": "Team",
                    "value": "Team",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {"label": "Enter Here", "value": "x", "activators": []}
                        ]
                    },
                },
                {
                    "label": "Cost Centre",
                    "value": "Cost Centre",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {"label": "Enter Here", "value": "x", "activators": []}
                        ]
                    },
                },
                {
                    "label": "Reporting To",
                    "value": "Reporting To",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Surname",
                                "value": "Richardson",
                                "activators": [],
                            },
                            {"label": "Forename", "value": "Mark ", "activators": []},
                        ]
                    },
                },
                {
                    "label": "Closing Date",
                    "value": "Closing Date",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {"label": "Enter", "value": "31/01/2020", "activators": []}
                        ]
                    },
                },
            ]
        },
        "customFields": {"customField": description},
        "customLovs": {
            "customLov": [
                {
                    "label": "Reason for Fixed Term/Secondment",
                    "value": "Reason for Fixed TermSecondment",
                    "order": 5,
                    "parents": None,
                    "criteria": {
                        "criterion": [{"label": "N/A", "value": "NA", "activators": []}]
                    },
                },
                {
                    "label": "Job Group",
                    "value": "Job Group",
                    "order": 8,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {"label": job_group, "value": job_group, "activators": []}
                        ]
                    },
                },
                {
                    "label": "Location",
                    "value": "Location",
                    "order": 2,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Aylesbury",
                                "value": "Aylesbury",
                                "activators": [],
                            }
                        ]
                    },
                },
                {
                    "label": "Show Apply Button",
                    "value": "Show Apply Button",
                    "order": 14,
                    "parents": None,
                    "criteria": {
                        "criterion": [{"label": "No", "value": "No", "activators": []}]
                    },
                },
                {
                    "label": "Salary Range - FTE",
                    "value": "Salary Range  FTE",
                    "order": 10,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "£21,807 - £23,570",
                                "value": "Schools Bucks Pay Range 3",
                                "activators": [],
                            }
                        ]
                    },
                },
                {
                    "label": "Searchable Salary",
                    "value": "Searchable Salary",
                    "order": 15,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Up to £20,000",
                                "value": "Up to 20000",
                                "activators": [],
                            }
                        ]
                    },
                },
                {
                    "label": "Grade / Range From:",
                    "value": "Grade  Range From",
                    "order": 3,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {"label": "Range 3", "value": "Range 3", "activators": []}
                        ]
                    },
                },
                {
                    "label": "Type of photo for advert",
                    "value": "Type of photo for advert",
                    "order": 23,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "SchoolsPrimaryRed",
                                "value": "SchoolsPrimaryRed",
                                "activators": [],
                            }
                        ]
                    },
                },
                {
                    "label": "Searchable Location",
                    "value": "Searchable Location",
                    "order": 17,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Aylesbury Vale",
                                "value": "Aylesbury Vale",
                                "activators": [],
                            }
                        ]
                    },
                },
                {
                    "label": "Working Hours Selection",
                    "value": "Working Hours Selection",
                    "order": 11,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Full Time",
                                "value": "Full Time",
                                "activators": [],
                            }
                        ]
                    },
                },
            ]
        },
        "dueDate": None,
        "duration": None,
        "expectedEndDate": None,
        "expectedStartDate": None,
        "externalJobNumber": None,
        "generalApplication": False,
        "id": talentlink_id,
        "jobNumber": job_number,
        "jobTitle": title,
        "keyword": None,
        "language": "UK",
        "location": None,
        "operationals": None,
        "organizations": {
            "organization": [
                {
                    "label": "Future Shape",
                    "value": "Future Shape",
                    "level": 1,
                    "suborganizations": None,
                },
                {
                    "label": "Schools",
                    "value": "Schools",
                    "level": 2,
                    "suborganizations": None,
                },
            ]
        },
        "postingEndDate": datetime.datetime(
            2020, 1, 31, 23, 59, 59, tzinfo=pytz.FixedOffset(60)
        ),
        "postingStartDate": datetime.datetime(
            2020, 1, 15, 0, 0, tzinfo=pytz.FixedOffset(60)
        ),
        "postingTargetStatus": "Published",
        "recruiters": {
            "recruiter": [
                {
                    "order": 1,
                    "value": "Example User",
                    "email": "example_user@buckscc.gov.uk",
                }
            ]
        },
        "recruitingCompany": None,
        "showCompensation": False,
        "showRecruiter": False,
        "siteLanguage": "UK",
        "standardLovs": {
            "standardLov": [
                {
                    "label": "Contract Type",
                    "value": "ContractType",
                    "order": None,
                    "parents": None,
                    "criteria": {
                        "criterion": [
                            {
                                "label": "Permanent",
                                "value": "Unlimited contract",
                                "activators": [],
                            }
                        ]
                    },
                }
            ]
        },
        "status": "Open",
        "strapline": None,
        "assignedImages": None,
        "requisitionInternalJobNumber": None,
        "jobLocations": None,
        "sponsoredJobContext": None,
        "jobUpdateDate": datetime.datetime(
            2020, 1, 15, 14, 11, 39, tzinfo=pytz.FixedOffset(60)
        ),
        "descriptionUrl": "http://jobs.buckscc.gov.uk/job-search?nPostingTargetId=164579&id=QQPFK026203F3VBQBV7V779XA&LG=UK&languageSelect=UK",  # noqa
        "postingUserEmail": "example_user@buckscc.gov.uk",
        "indeedConfiguration": None,
        "contractCompensationPeriod": None,
        "contractDuration": None,
        "standardRate": None,
    }
