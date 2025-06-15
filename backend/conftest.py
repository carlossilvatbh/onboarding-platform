"""
Configuração global de testes para o projeto ONBOARDING
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import factory
from datetime import date, datetime
from decimal import Decimal

from apps.kyc.models import KYCProfile, UBODeclaration, PEPDeclaration


# Factories para criação de dados de teste
class UserFactory(factory.django.DjangoModelFactory):
    """Factory para criação de usuários"""
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class KYCProfileFactory(factory.django.DjangoModelFactory):
    """Factory para criação de perfis KYC"""
    
    class Meta:
        model = KYCProfile
    
    user = factory.SubFactory(UserFactory)
    status = 'pending'
    full_name = factory.Faker('name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=80)
    nationality = factory.Faker('country')
    document_number = factory.Faker('ssn')
    document_type = 'passport'
    address_line1 = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    postal_code = factory.Faker('postcode')
    country = factory.Faker('country')
    occupation = factory.Faker('job')
    employer = factory.Faker('company')
    annual_income = factory.Faker('pydecimal', left_digits=6, right_digits=2, positive=True)
    source_of_funds = factory.Faker('text', max_nb_chars=200)


class UBODeclarationFactory(factory.django.DjangoModelFactory):
    """Factory para criação de declarações UBO"""
    
    class Meta:
        model = UBODeclaration
    
    kyc_profile = factory.SubFactory(KYCProfileFactory)
    full_name = factory.Faker('name')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=80)
    nationality = factory.Faker('country')
    ownership_percentage = factory.Faker('pydecimal', left_digits=2, right_digits=2, 
                                       positive=True, min_value=1, max_value=100)
    address_line1 = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state')
    postal_code = factory.Faker('postcode')
    country = factory.Faker('country')


class PEPDeclarationFactory(factory.django.DjangoModelFactory):
    """Factory para criação de declarações PEP"""
    
    class Meta:
        model = PEPDeclaration
    
    kyc_profile = factory.SubFactory(KYCProfileFactory)
    is_pep = False
    pep_type = ''
    position_held = ''
    organization = ''
    country = ''


# Fixtures básicas
@pytest.fixture
def user():
    """Fixture para usuário básico"""
    return UserFactory()


@pytest.fixture
def staff_user():
    """Fixture para usuário staff"""
    return UserFactory(is_staff=True)


@pytest.fixture
def superuser():
    """Fixture para superusuário"""
    return UserFactory(is_superuser=True, is_staff=True)


@pytest.fixture
def kyc_profile(user):
    """Fixture para perfil KYC"""
    return KYCProfileFactory(user=user)


@pytest.fixture
def approved_kyc_profile(user):
    """Fixture para perfil KYC aprovado"""
    return KYCProfileFactory(user=user, status='approved')


@pytest.fixture
def ubo_declaration(kyc_profile):
    """Fixture para declaração UBO"""
    return UBODeclarationFactory(kyc_profile=kyc_profile, ownership_percentage=Decimal('50.00'))


@pytest.fixture
def pep_declaration(kyc_profile):
    """Fixture para declaração PEP (não-PEP)"""
    return PEPDeclarationFactory(kyc_profile=kyc_profile, is_pep=False)


@pytest.fixture
def pep_declaration_positive(kyc_profile):
    """Fixture para declaração PEP positiva"""
    return PEPDeclarationFactory(
        kyc_profile=kyc_profile,
        is_pep=True,
        pep_type='domestic',
        position_held='Minister',
        organization='Government',
        country='Brazil'
    )


# Fixtures para clientes de teste
@pytest.fixture
def client():
    """Cliente Django básico"""
    return Client()


@pytest.fixture
def api_client():
    """Cliente API REST básico"""
    return APIClient()


@pytest.fixture
def authenticated_client(user):
    """Cliente autenticado"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def staff_client(staff_user):
    """Cliente autenticado como staff"""
    client = APIClient()
    client.force_authenticate(user=staff_user)
    return client


@pytest.fixture
def token_client(user):
    """Cliente com autenticação por token"""
    token, created = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


# Fixtures para dados de teste
@pytest.fixture
def sample_kyc_data():
    """Dados de exemplo para criação de perfil KYC"""
    return {
        'full_name': 'João Silva',
        'date_of_birth': date(1990, 1, 1),
        'nationality': 'Brazilian',
        'document_number': '123456789',
        'document_type': 'passport',
        'address_line1': 'Rua das Flores, 123',
        'city': 'São Paulo',
        'state': 'SP',
        'postal_code': '01234-567',
        'country': 'Brazil',
        'occupation': 'Software Engineer',
        'employer': 'Tech Company',
        'annual_income': Decimal('120000.00'),
        'source_of_funds': 'Employment salary and investments'
    }


@pytest.fixture
def sample_ubo_data():
    """Dados de exemplo para declaração UBO"""
    return {
        'full_name': 'Maria Santos',
        'date_of_birth': date(1985, 5, 15),
        'nationality': 'Brazilian',
        'ownership_percentage': Decimal('75.00'),
        'address_line1': 'Av. Paulista, 1000',
        'city': 'São Paulo',
        'state': 'SP',
        'postal_code': '01310-100',
        'country': 'Brazil'
    }


@pytest.fixture
def sample_pep_data():
    """Dados de exemplo para declaração PEP"""
    return {
        'is_pep': True,
        'pep_type': 'domestic',
        'position_held': 'City Councilor',
        'organization': 'São Paulo City Council',
        'country': 'Brazil',
        'start_date': date(2020, 1, 1),
        'end_date': date(2024, 12, 31)
    }


# Fixtures para cenários específicos
@pytest.fixture
def complete_kyc_profile(user, sample_kyc_data):
    """Perfil KYC completo com UBO e PEP"""
    profile = KYCProfileFactory(user=user, **sample_kyc_data)
    
    # Adicionar UBO
    UBODeclarationFactory(
        kyc_profile=profile,
        ownership_percentage=Decimal('100.00')
    )
    
    # Adicionar PEP
    PEPDeclarationFactory(
        kyc_profile=profile,
        is_pep=False
    )
    
    return profile


@pytest.fixture
def multiple_ubos_profile(user):
    """Perfil KYC com múltiplos UBOs"""
    profile = KYCProfileFactory(user=user)
    
    # Criar múltiplos UBOs que somam 100%
    UBODeclarationFactory(kyc_profile=profile, ownership_percentage=Decimal('60.00'))
    UBODeclarationFactory(kyc_profile=profile, ownership_percentage=Decimal('40.00'))
    
    return profile


@pytest.fixture
def invalid_ubos_profile(user):
    """Perfil KYC com UBOs inválidos (soma > 100%)"""
    profile = KYCProfileFactory(user=user)
    
    # Criar UBOs que somam mais de 100%
    UBODeclarationFactory(kyc_profile=profile, ownership_percentage=Decimal('70.00'))
    UBODeclarationFactory(kyc_profile=profile, ownership_percentage=Decimal('50.00'))
    
    return profile


# Configurações de banco de dados para testes
@pytest.fixture(scope='session')
def django_db_setup():
    """Configuração do banco de dados para testes"""
    from django.conf import settings
    from django.test.utils import setup_test_environment, teardown_test_environment
    
    setup_test_environment()
    yield
    teardown_test_environment()


# Marks personalizados
pytestmark = pytest.mark.django_db

