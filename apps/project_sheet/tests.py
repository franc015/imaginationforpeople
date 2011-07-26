"""
Example on how to use tests for TDD
"""
from django.test import TestCase

from apps.project_sheet.models import I4pProject, I4pProjectTranslation

from utils import create_parent_project, get_project_translation_by_slug
from utils import get_project_translation_from_parent

class TestUtils(TestCase):
    fixtures = ["test_pjsheet"]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_parent_project(self):
        project = create_parent_project()
        self.assertTrue(project.pk  > 0)
        

    def test_get_project_translation_by_slug(self):
        # Existing project
        translation = get_project_translation_by_slug('boby-a-la-mer', 'fr')
        self.assertEqual(translation.slug, 'boby-a-la-mer')

        # Existing slug but not in this language
        self.assertRaises(I4pProjectTranslation.DoesNotExist,
                          get_project_translation_by_slug,
                          (),
                          {'project_translation_slug': 'boby-a-la-mer',
                           'language_code': 'en'}
                          )

        # Non-existent slug (in any language)
        self.assertRaises(I4pProjectTranslation.DoesNotExist,
                          get_project_translation_by_slug,
                          (),
                          {'project_translation_slug': 'non-existent-slug',
                           'language_code': 'en'}
                          )


        # Existing slug but incorrect language
        self.assertRaises(I4pProjectTranslation.DoesNotExist,
                          get_project_translation_by_slug,
                          (),
                          {'project_translation_slug': 'boby-a-la-mer',
                           'language_code': 'kk'}
                          )

        # Non-existing slug and incorrect language
        self.assertRaises(I4pProjectTranslation.DoesNotExist,
                          get_project_translation_by_slug,
                          project_translation_slug='non-existing-slug',
                          language_code='kk'
                          )


    def test_project_translation_from_parent(self):
        # Get an existing translation and project
        translation_fr = get_project_translation_by_slug(project_translation_slug='boby-a-la-mer', 
                                                         language_code='fr')
        parent = translation_fr.project

        # Existing one
        requested_translation = get_project_translation_from_parent(parent=parent, 
                                                                    language_code='fr')
        self.assertEqual(translation_fr, requested_translation)

        # If two translations have the same slug, make sure the
        # correct one is returned
        requested_translation = get_project_translation_from_parent(parent=parent, 
                                                                    language_code='zh')
        self.assertNotEqual(translation_fr, requested_translation)

        # Non-existing one in the given language but in the fallback language
        requested_translation = get_project_translation_from_parent(parent=parent, 
                                                                    language_code='kk',
                                                                    fallback_language='fr')
        self.assertEqual(requested_translation, translation_fr)

        # Non-existing one in the given language neither in the fallback language
        self.assertRaises(I4pProjectTranslation.DoesNotExist,
                          get_project_translation_from_parent,
                          parent=parent,
                          language_code='kk',
                          fallback_language='en'
                          )
        
        # Parent is None
        self.assertRaises(I4pProject.DoesNotExist,
                          get_project_translation_from_parent,
                          parent=None,
                          language_code='fr',
                          )

        # If both the language code and the fallback language don't
        # exist, make sure fallback_any works.
        requested_translation = get_project_translation_from_parent(parent=parent, 
                                                                    language_code='kk',
                                                                    fallback_language='pm',
                                                                    fallback_any=True)

        self.assertTrue(isinstance(requested_translation, I4pProjectTranslation))
        self.assertEqual(requested_translation.project, parent)

        
        

        











