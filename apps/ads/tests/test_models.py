from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Ad, ExchangeProposal


class AdModelTest(TestCase):
    """Тесты модели Ad"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_ad_creation(self):
        """Тест создания объявления"""
        ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test description',
            category='electronics',
            condition='new'
        )
        self.assertEqual(ad.title, 'Test Ad')
        self.assertEqual(ad.user, self.user)
        self.assertEqual(str(ad), 'Test Ad')

    def test_ad_str_representation(self):
        """Тест строкового представления модели Ad"""
        ad = Ad.objects.create(
            user=self.user,
            title='Test Ad Title',
            description='Test description',
            category='books',
            condition='used'
        )
        self.assertEqual(str(ad), 'Test Ad Title')

    def test_str_model_ad(self):
        """Тест строкового представления модели Ad"""
        ad = Ad.objects.create(
            user=self.user,
            title='Test Ad Title',
            description='Test description',
        )
        self.assertEqual(str(ad), 'Test Ad Title')


class ExchangeProposalModelTest(TestCase):
    """Тесты модели ExchangeProposal"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='pass123'
        )
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Ad 1',
            description='Description 1',
            category='electronics',
            condition='new'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Ad 2',
            description='Description 2',
            category='books',
            condition='used'
        )

    def test_exchange_proposal_creation(self):
        """Тест создания предложения обмена"""
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Test comment'
        )
        self.assertEqual(proposal.ad_sender, self.ad1)
        self.assertEqual(proposal.ad_receiver, self.ad2)
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.comment, 'Test comment')

    def test_exchange_proposal_str_representation(self):
        """Тест строкового представления модели ExchangeProposal"""
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Test comment'
        )
        expected_str = f'Обменять {self.ad1} на {self.ad2} [pending]'
        self.assertEqual(str(proposal), expected_str)
