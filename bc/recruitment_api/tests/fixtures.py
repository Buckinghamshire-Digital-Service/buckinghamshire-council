import datetime

import pytz

no_further_pages_response = {"advertisements": None, "totalResults": 143}


def get_advertisement(
    job_number="FS11605",
    talentlink_id=164579,
    title="Higher Level Teaching Assistant - Elmhurst School ",
    description=None,
):
    if description is None:
        description = [
            {
                "label": "Overview",
                "order": 1,
                "value": """<p>Required for 24th February 2020 (or as close to as
                possible)</p>\n<p>Salary: Bucks Pay Range 3 Scale 16 - 20</p>\n<p>Full
                Time 08:15 – 15:45 Term Time Only (+5 INSET Days)</p>\n<p><strong>Are
                you a dynamic and compassionate practitioner with the capacity to grow
                and develop within a growing team? </strong></p>\n<p><strong>We are
                looking for a Higher-Level Teaching Assistant with experience of
                teaching whole classes in the Early Years Foundation
                Stage.</strong></p>\n<p>In joining Elmhurst School and the Great
                Learners Trust you will benefit from being a part of a dynamic and
                forward-thinking Multi-Academy Trust.</p>""",  # noqa
            },
            {
                "label": "About us",
                "order": 2,
                "value": '<p><strong>Elmhurst Values are: Aspire, Create, Think</strong></p>\n<p>Our GLT motto is<strong> "Believe and Achieve"</strong>, which reflects the determination of the Trust to expect great things for all our children, whatever their prior attainment.</p>\n<p>The vision of the Great Learners Trust is that all children in the Multi-Academy Trust community of schools are provided with outstanding educational opportunities.</p>\n<p>Our purpose is the best education for all children, regardless of their starting points, their individual learning needs, their level of disadvantage or advantage, their family background or their beliefs.</p>\n<p>We aim for:</p>\n<p>Challenge for All – Growth Mindset in Action</p>\n<p>Exceptional Progress</p>\n<p>Unforgettable Learning Experiences</p>\n<p>The Great Learners Trust believes that every child can be a great learner – it is our job to make that happen.</p>\n<p>Websites: http://www.elmhurstschool.org and http://www.greatlearnerstrust.co.uk/</p>',  # noqa
            },
            {
                "label": "About the role",
                "order": 3,
                "value": "<p>The HLTA is responsible for supporting the delivery of teaching and learning in Early Years Foundation Stage (2YOs, Nursery & Reception). Their timetable will be flexible and will include supporting a class teacher, delivery of lessons on both a regular and ad hoc basis (e.g. to cover first day sickness or courses).</p>\n<p>For more information please see attached Job description below.\xa0</p>",  # noqa
            },
            {
                "label": "About you",
                "order": 4,
                "value": "<p>We are looking for a Higher-Level Teaching Assistant who:</p>\n<p>Has confidence in themselves to effectively teach, manage behaviour and build strong, positive relationships.</p>\n<p>Is flexible, open minded and able to think on his/her feet.</p>\n<p>Is able to motivate pupils and staff within the team to ensure the best results are achieved.</p>\n<p>Has energy, enthusiasm and a growth mindset</p>\n<p>For more information please see attached Person specification below.\xa0</p>",  # noqa
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
        "applicationUrl": "https://www.example.com/",
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
                            {
                                "label": "Schools & Early Years - Support",
                                "value": "Schools  Early Years  Support",
                                "activators": [],
                            }
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
