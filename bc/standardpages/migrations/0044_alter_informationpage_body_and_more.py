# Generated by Django 4.2.19 on 2025-02-24 14:40

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        (
            "standardpages",
            "0043_directory_search_block__add_bucks_online_directory_option",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="informationpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("heading", 0),
                    ("subheading", 1),
                    ("paragraph", 2),
                    ("image", 6),
                    ("embed", 7),
                    ("local_area_links", 16),
                    ("plain_text_table", 17),
                    ("table", 23),
                    ("button", 27),
                    ("highlight", 28),
                    ("inset_text", 29),
                    ("ehc_co_search", 30),
                    ("directory_search", 35),
                    ("form", 36),
                    ("accordion", 41),
                    ("detail", 44),
                ],
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "group": "Heading",
                            "help_text": 'The link to this heading uses the heading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            "icon": "title",
                            "label": "Main heading",
                            "template": "patterns/molecules/streamfield/blocks/heading_block.html",
                        },
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "group": "Heading",
                            "help_text": 'The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            "icon": "title",
                            "template": "patterns/molecules/streamfield/blocks/subheading_block.html",
                        },
                    ),
                    2: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ]
                        },
                    ),
                    3: ("wagtail.images.blocks.ImageChooserBlock", (), {}),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Describe the information, not the picture. Leave blank if the image is purely decorative. Do not repeat captions or content already on the page.",
                            "required": False,
                        },
                    ),
                    5: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 3), ("alt_text", 4), ("caption", 5)]],
                        {},
                    ),
                    7: ("wagtail.embeds.blocks.EmbedBlock", (), {}),
                    8: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p><b>Find local information</b></p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                        },
                    ),
                    9: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p>While we finish building this new website, we’re keeping some local information on our old council websites</p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                        },
                    ),
                    10: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p>Enter your postcode to help us redirect you to the right place.</p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                            "help_text": "The text that appears on top of the postcode lookup input",
                        },
                    ),
                    11: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p>Select your local area to help us direct you to the right place:</p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                            "help_text": "The text that appears on top of the list of local area links",
                        },
                    ),
                    12: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {"label": "Aylesbury Vale URL"},
                    ),
                    13: ("wagtail.blocks.URLBlock", (), {"label": "Chiltern URL"}),
                    14: ("wagtail.blocks.URLBlock", (), {"label": "South Bucks URL"}),
                    15: ("wagtail.blocks.URLBlock", (), {"label": "Wycombe URL"}),
                    16: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("heading", 8),
                                ("introduction", 9),
                                ("postcode_lookup_text", 10),
                                ("area_lookup_text", 11),
                                ("aylesbury_vale_url", 12),
                                ("chiltern_url", 13),
                                ("south_bucks_url", 14),
                                ("wycombe_url", 15),
                            ]
                        ],
                        {},
                    ),
                    17: (
                        "bc.utils.blocks.TableBlock",
                        (),
                        {
                            "group": "Table",
                            "help_text": 'This table will be displayed as plain text on the page.\n    You can add links to individuals cells by using the following\n    syntax: <em>[link text](www.gov.uk)</em>. This will output as\n    <a href="http://www.gov.uk">link text</a></li>',
                        },
                    ),
                    18: ("wagtail.blocks.DecimalBlock", (), {}),
                    19: ("wagtail.blocks.RichTextBlock", (), {}),
                    20: (
                        "wagtail.blocks.StreamBlock",
                        [[("numeric", 18), ("rich_text", 19)]],
                        {},
                    ),
                    21: (
                        "wagtail.contrib.typed_table_block.blocks.TypedTableBlock",
                        [[("left_aligned_column", 20), ("right_aligned_column", 20)]],
                        {},
                    ),
                    22: ("wagtail.blocks.TextBlock", (), {"required": False}),
                    23: (
                        "wagtail.blocks.StructBlock",
                        [[("table", 21), ("caption", 22)]],
                        {"group": "Table"},
                    ),
                    24: ("wagtail.blocks.CharBlock", (), {"form_classname": "title"}),
                    25: ("wagtail.blocks.URLBlock", (), {"required": False}),
                    26: ("wagtail.blocks.PageChooserBlock", (), {"required": False}),
                    27: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 24), ("link_url", 25), ("link_page", 26)]],
                        {},
                    ),
                    28: ("bc.utils.blocks.HighlightBlock", (), {}),
                    29: ("bc.utils.blocks.InsetTextBlock", (), {}),
                    30: (
                        "bc.utils.blocks.EHCCoSearchBlock",
                        (),
                        {"label": "EHCCo Search"},
                    ),
                    31: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"help_text": "Title of the widget", "required": True},
                    ),
                    32: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Placeholder text for the search input",
                            "required": False,
                        },
                    ),
                    33: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("bucks_online_directory", "Bucks Online Directory"),
                                ("familyinfo", "Family Information Service"),
                                ("send", "SEND"),
                            ],
                            "help_text": "Which directory to search",
                        },
                    ),
                    34: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Extra query parameters to add to the search, e.g. ?collection=things-to-do&needs=autism",
                            "required": False,
                        },
                    ),
                    35: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 31),
                                ("search_placeholder", 32),
                                ("directory", 33),
                                ("extra_query_params", 34),
                            ]
                        ],
                        {},
                    ),
                    36: ("bc.forms.blocks.EmbeddedFormBlock", (), {}),
                    37: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "icon": "title",
                            "label": "Accordion title",
                        },
                    ),
                    38: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("heading", 0),
                                ("subheading", 1),
                                ("paragraph", 2),
                                ("image", 6),
                                ("embed", 7),
                                ("local_area_links", 16),
                                ("plain_text_table", 17),
                                ("table", 23),
                                ("button", 27),
                                ("highlight", 28),
                                ("inset_text", 29),
                                ("ehc_co_search", 30),
                                ("directory_search", 35),
                                ("form", 36),
                            ]
                        ],
                        {"label": "Accordion content"},
                    ),
                    39: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 37), ("content", 38)]],
                        {},
                    ),
                    40: (
                        "wagtail.blocks.ListBlock",
                        (39,),
                        {"label": "Accordion items"},
                    ),
                    41: ("wagtail.blocks.StructBlock", [[("items", 40)]], {}),
                    42: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "icon": "title",
                            "label": "Detail title",
                        },
                    ),
                    43: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                            "label": "Detail content",
                        },
                    ),
                    44: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 42), ("content", 43)]],
                        {},
                    ),
                },
            ),
        ),
        migrations.AlterField(
            model_name="wastewizardpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("heading", 0),
                    ("subheading", 1),
                    ("paragraph", 2),
                    ("image", 6),
                    ("embed", 7),
                    ("local_area_links", 16),
                    ("plain_text_table", 17),
                    ("table", 23),
                    ("button", 27),
                    ("highlight", 28),
                    ("inset_text", 29),
                    ("ehc_co_search", 30),
                    ("directory_search", 35),
                    ("form", 36),
                    ("accordion", 41),
                    ("detail", 44),
                    ("waste_wizard", 45),
                ],
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "group": "Heading",
                            "help_text": 'The link to this heading uses the heading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            "icon": "title",
                            "label": "Main heading",
                            "template": "patterns/molecules/streamfield/blocks/heading_block.html",
                        },
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "group": "Heading",
                            "help_text": 'The link to this subheading uses the subheading text in lowercase, with no symbols, and with the spaces replaced with hyphens. e.g. "Lorem @ 2 ipsum" becomes "lorem-2-ipsum"',
                            "icon": "title",
                            "template": "patterns/molecules/streamfield/blocks/subheading_block.html",
                        },
                    ),
                    2: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ]
                        },
                    ),
                    3: ("wagtail.images.blocks.ImageChooserBlock", (), {}),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Describe the information, not the picture. Leave blank if the image is purely decorative. Do not repeat captions or content already on the page.",
                            "required": False,
                        },
                    ),
                    5: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 3), ("alt_text", 4), ("caption", 5)]],
                        {},
                    ),
                    7: ("wagtail.embeds.blocks.EmbedBlock", (), {}),
                    8: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p><b>Find local information</b></p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                        },
                    ),
                    9: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p>While we finish building this new website, we’re keeping some local information on our old council websites</p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                        },
                    ),
                    10: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p>Enter your postcode to help us redirect you to the right place.</p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                            "help_text": "The text that appears on top of the postcode lookup input",
                        },
                    ),
                    11: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "default": "<p>Select your local area to help us direct you to the right place:</p>",
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                            "help_text": "The text that appears on top of the list of local area links",
                        },
                    ),
                    12: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {"label": "Aylesbury Vale URL"},
                    ),
                    13: ("wagtail.blocks.URLBlock", (), {"label": "Chiltern URL"}),
                    14: ("wagtail.blocks.URLBlock", (), {"label": "South Bucks URL"}),
                    15: ("wagtail.blocks.URLBlock", (), {"label": "Wycombe URL"}),
                    16: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("heading", 8),
                                ("introduction", 9),
                                ("postcode_lookup_text", 10),
                                ("area_lookup_text", 11),
                                ("aylesbury_vale_url", 12),
                                ("chiltern_url", 13),
                                ("south_bucks_url", 14),
                                ("wycombe_url", 15),
                            ]
                        ],
                        {},
                    ),
                    17: (
                        "bc.utils.blocks.TableBlock",
                        (),
                        {
                            "group": "Table",
                            "help_text": 'This table will be displayed as plain text on the page.\n    You can add links to individuals cells by using the following\n    syntax: <em>[link text](www.gov.uk)</em>. This will output as\n    <a href="http://www.gov.uk">link text</a></li>',
                        },
                    ),
                    18: ("wagtail.blocks.DecimalBlock", (), {}),
                    19: ("wagtail.blocks.RichTextBlock", (), {}),
                    20: (
                        "wagtail.blocks.StreamBlock",
                        [[("numeric", 18), ("rich_text", 19)]],
                        {},
                    ),
                    21: (
                        "wagtail.contrib.typed_table_block.blocks.TypedTableBlock",
                        [[("left_aligned_column", 20), ("right_aligned_column", 20)]],
                        {},
                    ),
                    22: ("wagtail.blocks.TextBlock", (), {"required": False}),
                    23: (
                        "wagtail.blocks.StructBlock",
                        [[("table", 21), ("caption", 22)]],
                        {"group": "Table"},
                    ),
                    24: ("wagtail.blocks.CharBlock", (), {"form_classname": "title"}),
                    25: ("wagtail.blocks.URLBlock", (), {"required": False}),
                    26: ("wagtail.blocks.PageChooserBlock", (), {"required": False}),
                    27: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 24), ("link_url", 25), ("link_page", 26)]],
                        {},
                    ),
                    28: ("bc.utils.blocks.HighlightBlock", (), {}),
                    29: ("bc.utils.blocks.InsetTextBlock", (), {}),
                    30: (
                        "bc.utils.blocks.EHCCoSearchBlock",
                        (),
                        {"label": "EHCCo Search"},
                    ),
                    31: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"help_text": "Title of the widget", "required": True},
                    ),
                    32: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Placeholder text for the search input",
                            "required": False,
                        },
                    ),
                    33: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("bucks_online_directory", "Bucks Online Directory"),
                                ("familyinfo", "Family Information Service"),
                                ("send", "SEND"),
                            ],
                            "help_text": "Which directory to search",
                        },
                    ),
                    34: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Extra query parameters to add to the search, e.g. ?collection=things-to-do&needs=autism",
                            "required": False,
                        },
                    ),
                    35: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 31),
                                ("search_placeholder", 32),
                                ("directory", 33),
                                ("extra_query_params", 34),
                            ]
                        ],
                        {},
                    ),
                    36: ("bc.forms.blocks.EmbeddedFormBlock", (), {}),
                    37: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "icon": "title",
                            "label": "Accordion title",
                        },
                    ),
                    38: (
                        "wagtail.blocks.StreamBlock",
                        [
                            [
                                ("heading", 0),
                                ("subheading", 1),
                                ("paragraph", 2),
                                ("image", 6),
                                ("embed", 7),
                                ("local_area_links", 16),
                                ("plain_text_table", 17),
                                ("table", 23),
                                ("button", 27),
                                ("highlight", 28),
                                ("inset_text", 29),
                                ("ehc_co_search", 30),
                                ("directory_search", 35),
                                ("form", 36),
                            ]
                        ],
                        {"label": "Accordion content"},
                    ),
                    39: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 37), ("content", 38)]],
                        {},
                    ),
                    40: (
                        "wagtail.blocks.ListBlock",
                        (39,),
                        {"label": "Accordion items"},
                    ),
                    41: ("wagtail.blocks.StructBlock", [[("items", 40)]], {}),
                    42: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "full title",
                            "icon": "title",
                            "label": "Detail title",
                        },
                    ),
                    43: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                            ],
                            "label": "Detail content",
                        },
                    ),
                    44: (
                        "wagtail.blocks.StructBlock",
                        [[("title", 42), ("content", 43)]],
                        {},
                    ),
                    45: ("bc.utils.blocks.WasteWizardSnippetBlock", (), {}),
                },
            ),
        ),
    ]
