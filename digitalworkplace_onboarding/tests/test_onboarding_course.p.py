from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestOnboardingCourse(common.TransactionCase):
    """The module ships one course and its lessons as data.

    The test asserts that the course exists, that the lessons are attached to
    it, and that the content is present without demo data — the module puts
    everything in ``data/`` precisely so a production database
    (``--without-demo=all``) gets the course too.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.channel = cls.env.ref(
            'digitalworkplace_onboarding.slide_channel_digitalworkplace',
            raise_if_not_found=False,
        )

    def test_01_channel_exists(self):
        """The course record must exist and be a published training channel."""
        self.assertTrue(self.channel, "The onboarding course was not created")
        self.assertEqual(self.channel.channel_type, 'training')
        self.assertTrue(self.channel.is_published)

    def test_02_channel_has_lessons(self):
        """The course must carry the five sections and their slides."""
        sections = self.channel.slide_ids.filtered('is_category')
        self.assertEqual(
            len(sections), 5,
            "Expected five section headers, got %s" % len(sections),
        )
        lessons = self.channel.slide_ids - sections
        self.assertTrue(
            lessons, "The course has no slides outside the section headers",
        )

    def test_03_lessons_are_published(self):
        """Every slide in the course is published so a learner can read it."""
        unpublished = self.channel.slide_ids.filtered(lambda s: not s.is_published)
        self.assertFalse(
            unpublished, "Unpublished slides: %s" % unpublished.mapped('name'),
        )

    def test_04_lessons_have_content(self):
        """Each non-category slide carries either html_content or a description."""
        empty = self.channel.slide_ids.filtered(
            lambda s: not s.is_category
            and not (s.html_content or s.description)
        )
        self.assertFalse(
            empty, "Slides without content: %s" % empty.mapped('name'),
        )

    def test_05_sections_are_ordered(self):
        """Section headers are numbered 1..5 in sequence order."""
        names = self.channel.slide_ids.filtered('is_category').sorted(
            'sequence').mapped('name')
        self.assertEqual(
            [n.split('.')[0] for n in names], ['1', '2', '3', '4', '5'],
        )
