# Generated by Django 2.2.15 on 2020-10-13 08:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("images", "0003_job_employer_logo"),
        ("documents", "0004_job_attachments"),
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
    ]

    operations = [
        migrations.CreateModel(
            name="LongformPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("social_text", models.CharField(blank=True, max_length=255)),
                (
                    "listing_title",
                    models.CharField(
                        blank=True,
                        help_text="Override the page title used when this page appears in listings",
                        max_length=255,
                    ),
                ),
                (
                    "listing_summary",
                    models.CharField(
                        blank=True,
                        help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                        max_length=255,
                    ),
                ),
                (
                    "redirect_to",
                    models.URLField(
                        blank=True,
                        help_text="Entering a URL here will prevent the page from being visited, and will instead redirect the user.",
                        verbose_name="Redirect to external URL",
                    ),
                ),
                (
                    "show_live_chat_client",
                    models.BooleanField(
                        default=False,
                        help_text="Show live chat support client on this page",
                    ),
                ),
                ("last_updated", models.DateField()),
                ("version_number", models.CharField(blank=True, max_length=100)),
                (
                    "chapter_heading",
                    models.CharField(
                        blank=True,
                        default="Introduction",
                        help_text='Optional, e.g. "Introduction", chapter heading that will appear before the body',
                        max_length=255,
                    ),
                ),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "heading",
                                wagtail.core.blocks.CharBlock(
                                    classname="full title",
                                    group="Heading",
                                    icon="title",
                                    label="Main heading",
                                    template="patterns/molecules/streamfield/blocks/heading_block.html",
                                ),
                            ),
                            (
                                "subheading",
                                wagtail.core.blocks.CharBlock(
                                    classname="full title",
                                    group="Heading",
                                    icon="title",
                                    template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                ),
                            ),
                            (
                                "paragraph",
                                wagtail.core.blocks.RichTextBlock(
                                    features=[
                                        "bold",
                                        "italic",
                                        "ol",
                                        "ul",
                                        "link",
                                        "document-link",
                                    ]
                                ),
                            ),
                            (
                                "image",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "caption",
                                            wagtail.core.blocks.CharBlock(
                                                required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            ("embed", wagtail.embeds.blocks.EmbedBlock()),
                            (
                                "local_area_links",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "introduction",
                                            wagtail.core.blocks.RichTextBlock(
                                                default="<p>Select your local area for information:</p>",
                                                features=[
                                                    "bold",
                                                    "italic",
                                                    "ol",
                                                    "ul",
                                                    "link",
                                                    "document-link",
                                                ],
                                            ),
                                        ),
                                        (
                                            "aylesbury_vale_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="Aylesbury Vale URL",
                                                required=False,
                                            ),
                                        ),
                                        (
                                            "chiltern_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="Chiltern URL", required=False
                                            ),
                                        ),
                                        (
                                            "south_bucks_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="South Bucks URL", required=False
                                            ),
                                        ),
                                        (
                                            "wycombe_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="Wycombe URL", required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                            (
                                "button",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            wagtail.core.blocks.CharBlock(
                                                classname="title"
                                            ),
                                        ),
                                        (
                                            "link_url",
                                            wagtail.core.blocks.URLBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            "link_page",
                                            wagtail.core.blocks.PageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "detail",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.core.blocks.CharBlock(
                                                classname="full title",
                                                icon="title",
                                                label="Detail title",
                                            ),
                                        ),
                                        (
                                            "content",
                                            wagtail.core.blocks.RichTextBlock(
                                                features=[
                                                    "bold",
                                                    "italic",
                                                    "ol",
                                                    "ul",
                                                    "link",
                                                    "document-link",
                                                ],
                                                label="Detail content",
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                (
                    "document_link_text",
                    models.CharField(
                        blank=True,
                        help_text='Optional, e.g. "Download the policy", defaults to the linked document\'s own title',
                        max_length=255,
                    ),
                ),
                (
                    "document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="documents.CustomDocument",
                    ),
                ),
                (
                    "listing_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the image you wish to be displayed when this page appears in listings",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
                (
                    "social_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Long-form content page",
            },
            bases=("wagtailcore.page", models.Model),
        ),
        migrations.CreateModel(
            name="LongformChapterPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("social_text", models.CharField(blank=True, max_length=255)),
                (
                    "listing_title",
                    models.CharField(
                        blank=True,
                        help_text="Override the page title used when this page appears in listings",
                        max_length=255,
                    ),
                ),
                (
                    "listing_summary",
                    models.CharField(
                        blank=True,
                        help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Meta description' field above is not defined.",
                        max_length=255,
                    ),
                ),
                (
                    "redirect_to",
                    models.URLField(
                        blank=True,
                        help_text="Entering a URL here will prevent the page from being visited, and will instead redirect the user.",
                        verbose_name="Redirect to external URL",
                    ),
                ),
                (
                    "show_live_chat_client",
                    models.BooleanField(
                        default=False,
                        help_text="Show live chat support client on this page",
                    ),
                ),
                (
                    "body",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "heading",
                                wagtail.core.blocks.CharBlock(
                                    classname="full title",
                                    group="Heading",
                                    icon="title",
                                    label="Main heading",
                                    template="patterns/molecules/streamfield/blocks/heading_block.html",
                                ),
                            ),
                            (
                                "subheading",
                                wagtail.core.blocks.CharBlock(
                                    classname="full title",
                                    group="Heading",
                                    icon="title",
                                    template="patterns/molecules/streamfield/blocks/subheading_block.html",
                                ),
                            ),
                            (
                                "paragraph",
                                wagtail.core.blocks.RichTextBlock(
                                    features=[
                                        "bold",
                                        "italic",
                                        "ol",
                                        "ul",
                                        "link",
                                        "document-link",
                                    ]
                                ),
                            ),
                            (
                                "image",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "caption",
                                            wagtail.core.blocks.CharBlock(
                                                required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            ("embed", wagtail.embeds.blocks.EmbedBlock()),
                            (
                                "local_area_links",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "introduction",
                                            wagtail.core.blocks.RichTextBlock(
                                                default="<p>Select your local area for information:</p>",
                                                features=[
                                                    "bold",
                                                    "italic",
                                                    "ol",
                                                    "ul",
                                                    "link",
                                                    "document-link",
                                                ],
                                            ),
                                        ),
                                        (
                                            "aylesbury_vale_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="Aylesbury Vale URL",
                                                required=False,
                                            ),
                                        ),
                                        (
                                            "chiltern_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="Chiltern URL", required=False
                                            ),
                                        ),
                                        (
                                            "south_bucks_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="South Bucks URL", required=False
                                            ),
                                        ),
                                        (
                                            "wycombe_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="Wycombe URL", required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                            (
                                "button",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            wagtail.core.blocks.CharBlock(
                                                classname="title"
                                            ),
                                        ),
                                        (
                                            "link_url",
                                            wagtail.core.blocks.URLBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            "link_page",
                                            wagtail.core.blocks.PageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "detail",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.core.blocks.CharBlock(
                                                classname="full title",
                                                icon="title",
                                                label="Detail title",
                                            ),
                                        ),
                                        (
                                            "content",
                                            wagtail.core.blocks.RichTextBlock(
                                                features=[
                                                    "bold",
                                                    "italic",
                                                    "ol",
                                                    "ul",
                                                    "link",
                                                    "document-link",
                                                ],
                                                label="Detail content",
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                (
                    "listing_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose the image you wish to be displayed when this page appears in listings",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
                (
                    "social_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.CustomImage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Long-form content chapter page",
            },
            bases=("wagtailcore.page", models.Model),
        ),
    ]
