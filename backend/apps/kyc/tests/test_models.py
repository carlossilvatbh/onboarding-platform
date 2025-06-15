"""
Testes para models do app KYC
Inclui testes para correções de bugs identificados no relatório
"""

import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

from apps.kyc.models import KYCProfile, UBODeclaration, PEPDeclaration, KYCDocument


@pytest.mark.django_db
@pytest.mark.models
class TestKYCProfile:
    """Testes para o modelo KYCProfile"""
    
    def test_create_kyc_profile(self, user, sample_kyc_data):
        """Teste criação de perfil KYC"""
        profile = KYCProfile.objects.create(user=user, **sample_kyc_data)
        
        assert profile.user == user
        assert profile.status == 'pending'
        assert profile.full_name == sample_kyc_data['full_name']
        assert str(profile) == f"KYC Profile - {profile.full_name} ({profile.status})"
    
    def test_kyc_profile_str_representation(self, kyc_profile):
        """Teste representação string do perfil KYC"""
        expected = f"KYC Profile - {kyc_profile.full_name} ({kyc_profile.status})"
        assert str(kyc_profile) == expected
    
    def test_kyc_profile_ordering(self, user):
        """Teste ordenação de perfis KYC"""
        profile1 = KYCProfile.objects.create(user=user, full_name="Profile 1")
        profile2 = KYCProfile.objects.create(user=user, full_name="Profile 2")
        
        profiles = list(KYCProfile.objects.all())
        assert profiles[0] == profile2  # Mais recente primeiro
        assert profiles[1] == profile1


@pytest.mark.django_db
@pytest.mark.models
class TestUBODeclaration:
    """
    Testes para o modelo UBODeclaration
    CORREÇÃO: Testes para bugs de validação UBO identificados
    """
    
    def test_create_ubo_declaration(self, kyc_profile, sample_ubo_data):
        """Teste criação de declaração UBO"""
        ubo = UBODeclaration.objects.create(kyc_profile=kyc_profile, **sample_ubo_data)
        
        assert ubo.kyc_profile == kyc_profile
        assert ubo.ownership_percentage == sample_ubo_data['ownership_percentage']
        assert str(ubo) == f"UBO: {ubo.full_name} ({ubo.ownership_percentage}%)"
    
    def test_get_ubos_for_profile_with_ubos(self, kyc_profile):
        """CORREÇÃO: Teste método seguro para obter UBOs quando existem"""
        ubo1 = UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="UBO 1",
            date_of_birth=date(1980, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('60.00'),
            address_line1="Address 1",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        ubo2 = UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="UBO 2",
            date_of_birth=date(1985, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('40.00'),
            address_line1="Address 2",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        ubos = UBODeclaration.get_ubos_for_profile(kyc_profile)
        
        assert len(ubos) == 2
        assert ubo1 in ubos
        assert ubo2 in ubos
    
    def test_get_ubos_for_profile_without_ubos(self, kyc_profile):
        """CORREÇÃO: Teste método seguro quando não há UBOs (evita TypeError)"""
        ubos = UBODeclaration.get_ubos_for_profile(kyc_profile)
        
        assert ubos == []
        assert isinstance(ubos, list)  # Sempre retorna lista, nunca None
    
    def test_validate_ubo_declarations_no_ubos(self, kyc_profile):
        """CORREÇÃO: Teste validação quando não há UBOs declarados"""
        validation = UBODeclaration.validate_ubo_declarations(kyc_profile)
        
        assert validation['is_valid'] is False
        assert 'No UBO declarations found' in validation['errors'][0]
        assert validation['total_percentage'] == 0
    
    def test_validate_ubo_declarations_valid(self, kyc_profile):
        """CORREÇÃO: Teste validação com UBOs válidos"""
        UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="Valid UBO",
            date_of_birth=date(1980, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('100.00'),
            address_line1="Address",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        validation = UBODeclaration.validate_ubo_declarations(kyc_profile)
        
        assert validation['is_valid'] is True
        assert validation['errors'] == []
        assert validation['total_percentage'] == 100
        assert validation['ubo_count'] == 1
    
    def test_validate_ubo_declarations_exceeds_100_percent(self, kyc_profile):
        """CORREÇÃO: Teste validação quando soma excede 100%"""
        UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="UBO 1",
            date_of_birth=date(1980, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('70.00'),
            address_line1="Address",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="UBO 2",
            date_of_birth=date(1985, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('50.00'),
            address_line1="Address",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        validation = UBODeclaration.validate_ubo_declarations(kyc_profile)
        
        assert validation['is_valid'] is False
        assert 'cannot exceed 100%' in validation['errors'][0]
        assert validation['total_percentage'] == 120
    
    def test_validate_ubo_declarations_below_25_percent(self, kyc_profile):
        """CORREÇÃO: Teste validação quando soma é menor que 25%"""
        UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="Small UBO",
            date_of_birth=date(1980, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('10.00'),
            address_line1="Address",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        validation = UBODeclaration.validate_ubo_declarations(kyc_profile)
        
        assert validation['is_valid'] is False
        assert 'At least 25% ownership must be declared' in validation['errors'][0]
        assert validation['total_percentage'] == 10
    
    def test_ubo_ordering(self, kyc_profile):
        """Teste ordenação de UBOs por percentual de propriedade"""
        ubo1 = UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="UBO 1",
            date_of_birth=date(1980, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('30.00'),
            address_line1="Address",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        ubo2 = UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="UBO 2",
            date_of_birth=date(1985, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('70.00'),
            address_line1="Address",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        ubos = list(UBODeclaration.objects.all())
        assert ubos[0] == ubo2  # Maior percentual primeiro
        assert ubos[1] == ubo1


@pytest.mark.django_db
@pytest.mark.models
class TestPEPDeclaration:
    """Testes para o modelo PEPDeclaration"""
    
    def test_create_non_pep_declaration(self, kyc_profile):
        """Teste criação de declaração não-PEP"""
        pep = PEPDeclaration.objects.create(
            kyc_profile=kyc_profile,
            is_pep=False
        )
        
        assert pep.kyc_profile == kyc_profile
        assert pep.is_pep is False
        assert str(pep) == f"Non-PEP: {kyc_profile.full_name}"
    
    def test_create_pep_declaration(self, kyc_profile):
        """Teste criação de declaração PEP"""
        pep = PEPDeclaration.objects.create(
            kyc_profile=kyc_profile,
            is_pep=True,
            pep_type='domestic',
            position_held='Minister',
            organization='Government',
            country='Brazil'
        )
        
        assert pep.is_pep is True
        assert pep.pep_type == 'domestic'
        assert str(pep) == f"PEP: {kyc_profile.full_name} - Minister"
    
    def test_pep_declaration_ordering(self, kyc_profile):
        """Teste ordenação de declarações PEP"""
        pep1 = PEPDeclaration.objects.create(kyc_profile=kyc_profile, is_pep=False)
        pep2 = PEPDeclaration.objects.create(kyc_profile=kyc_profile, is_pep=True)
        
        peps = list(PEPDeclaration.objects.all())
        assert peps[0] == pep2  # Mais recente primeiro
        assert peps[1] == pep1


@pytest.mark.django_db
@pytest.mark.models
class TestKYCDocument:
    """Testes para o modelo KYCDocument"""
    
    def test_create_kyc_document(self, kyc_profile):
        """Teste criação de documento KYC"""
        document = KYCDocument.objects.create(
            kyc_profile=kyc_profile,
            document_type='passport',
            original_filename='passport.pdf',
            file_size=1024000,
            mime_type='application/pdf'
        )
        
        assert document.kyc_profile == kyc_profile
        assert document.document_type == 'passport'
        assert document.ocr_processed is False
        assert str(document) == f"Passport - {kyc_profile.full_name}"
    
    def test_document_ordering(self, kyc_profile):
        """Teste ordenação de documentos"""
        doc1 = KYCDocument.objects.create(
            kyc_profile=kyc_profile,
            document_type='passport',
            original_filename='passport.pdf',
            file_size=1024000,
            mime_type='application/pdf'
        )
        
        doc2 = KYCDocument.objects.create(
            kyc_profile=kyc_profile,
            document_type='utility_bill',
            original_filename='bill.pdf',
            file_size=512000,
            mime_type='application/pdf'
        )
        
        docs = list(KYCDocument.objects.all())
        assert docs[0] == doc2  # Mais recente primeiro
        assert docs[1] == doc1
