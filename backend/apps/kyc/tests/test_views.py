"""
Testes para views do app KYC
Inclui testes para correções de paginação PEP identificadas no relatório
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

from apps.kyc.models import KYCProfile, UBODeclaration, PEPDeclaration, KYCDocument


@pytest.mark.django_db
@pytest.mark.api
@pytest.mark.views
class TestKYCProfileViewSet:
    """Testes para KYCProfileViewSet"""
    
    def test_list_kyc_profiles_authenticated(self, authenticated_client, kyc_profile):
        """Teste listagem de perfis KYC autenticado"""
        url = reverse('kyc:kycprofile-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == str(kyc_profile.id)
    
    def test_list_kyc_profiles_unauthenticated(self, api_client):
        """Teste listagem sem autenticação"""
        url = reverse('kyc:kycprofile-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_kyc_profile(self, authenticated_client, sample_kyc_data):
        """Teste criação de perfil KYC"""
        url = reverse('kyc:kycprofile-list')
        response = authenticated_client.post(url, sample_kyc_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == sample_kyc_data['full_name']
        assert response.data['status'] == 'pending'
    
    def test_submit_for_review_success(self, authenticated_client, kyc_profile):
        """Teste submissão para revisão com documentos"""
        # Criar documentos necessários
        KYCDocument.objects.create(
            kyc_profile=kyc_profile,
            document_type='passport',
            original_filename='passport.pdf',
            file_size=1024,
            mime_type='application/pdf'
        )
        KYCDocument.objects.create(
            kyc_profile=kyc_profile,
            document_type='utility_bill',
            original_filename='bill.pdf',
            file_size=1024,
            mime_type='application/pdf'
        )
        
        url = reverse('kyc:kycprofile-submit-for-review', kwargs={'pk': kyc_profile.id})
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        kyc_profile.refresh_from_db()
        assert kyc_profile.status == 'in_review'
    
    def test_submit_for_review_missing_documents(self, authenticated_client, kyc_profile):
        """Teste submissão sem documentos necessários"""
        url = reverse('kyc:kycprofile-submit-for-review', kwargs={'pk': kyc_profile.id})
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'missing' in response.data
    
    def test_validation_status_no_ubos(self, authenticated_client, kyc_profile):
        """CORREÇÃO: Teste status de validação sem UBOs"""
        url = reverse('kyc:kycprofile-validation-status', kwargs={'pk': kyc_profile.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['ubo_validation']['is_valid'] is False
        assert 'No UBO declarations found' in response.data['ubo_validation']['errors'][0]


@pytest.mark.django_db
@pytest.mark.api
@pytest.mark.views
class TestPEPDeclarationViewSet:
    """
    Testes para PEPDeclarationViewSet
    CORREÇÃO: Testes para paginação otimizada
    """
    
    def test_list_pep_declarations_with_pagination(self, authenticated_client, kyc_profile):
        """CORREÇÃO: Teste listagem com paginação otimizada"""
        # Criar múltiplas declarações PEP
        for i in range(15):
            PEPDeclaration.objects.create(
                kyc_profile=kyc_profile,
                is_pep=i % 2 == 0,  # Alternar entre PEP e não-PEP
                pep_type='domestic' if i % 2 == 0 else '',
                position_held=f'Position {i}' if i % 2 == 0 else '',
                organization=f'Org {i}' if i % 2 == 0 else ''
            )
        
        url = reverse('kyc:pepdeclaration-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data
        assert 'next' in response.data
        assert 'previous' in response.data
        
        # Verificar paginação (page_size = 10 para PEPs)
        assert len(response.data['results']) == 10
        assert response.data['count'] == 15
    
    def test_list_pep_declarations_with_search(self, authenticated_client, kyc_profile):
        """CORREÇÃO: Teste busca otimizada em declarações PEP"""
        PEPDeclaration.objects.create(
            kyc_profile=kyc_profile,
            is_pep=True,
            pep_type='domestic',
            position_held='Minister of Finance',
            organization='Government'
        )
        
        PEPDeclaration.objects.create(
            kyc_profile=kyc_profile,
            is_pep=True,
            pep_type='domestic',
            position_held='Mayor',
            organization='City Hall'
        )
        
        url = reverse('kyc:pepdeclaration-list')
        response = authenticated_client.get(url, {'search': 'Minister'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert 'Minister' in response.data['results'][0]['position_held']
    
    def test_pep_summary_endpoint(self, authenticated_client, kyc_profile):
        """CORREÇÃO: Teste endpoint de resumo otimizado"""
        # Criar declarações variadas
        PEPDeclaration.objects.create(kyc_profile=kyc_profile, is_pep=True, pep_type='domestic')
        PEPDeclaration.objects.create(kyc_profile=kyc_profile, is_pep=True, pep_type='foreign')
        PEPDeclaration.objects.create(kyc_profile=kyc_profile, is_pep=False)
        
        url = reverse('kyc:pepdeclaration-summary')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_declarations'] == 3
        assert response.data['pep_count'] == 2
        assert response.data['non_pep_count'] == 1
        assert 'by_type' in response.data
    
    def test_large_pep_list_performance(self, authenticated_client, kyc_profile):
        """CORREÇÃO: Teste performance com lista grande de PEPs"""
        # Criar muitas declarações PEP para testar paginação
        peps = []
        for i in range(100):
            peps.append(PEPDeclaration(
                kyc_profile=kyc_profile,
                is_pep=i % 3 == 0,
                pep_type='domestic' if i % 3 == 0 else '',
                position_held=f'Position {i}' if i % 3 == 0 else ''
            ))
        
        PEPDeclaration.objects.bulk_create(peps)
        
        url = reverse('kyc:pepdeclaration-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 10  # Paginação limitada
        assert response.data['count'] == 100


@pytest.mark.django_db
@pytest.mark.api
@pytest.mark.views
class TestUBODeclarationViewSet:
    """Testes para UBODeclarationViewSet"""
    
    def test_create_ubo_declaration_valid(self, authenticated_client, kyc_profile, sample_ubo_data):
        """Teste criação de declaração UBO válida"""
        sample_ubo_data['kyc_profile'] = kyc_profile.id
        
        url = reverse('kyc:ubodeclaration-list')
        response = authenticated_client.post(url, sample_ubo_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['ownership_percentage'] == str(sample_ubo_data['ownership_percentage'])
    
    def test_create_ubo_declaration_exceeds_100_percent(self, authenticated_client, kyc_profile):
        """Teste criação que excede 100% de propriedade"""
        # Criar UBO existente
        UBODeclaration.objects.create(
            kyc_profile=kyc_profile,
            full_name="Existing UBO",
            date_of_birth=date(1980, 1, 1),
            nationality="Brazilian",
            ownership_percentage=Decimal('70.00'),
            address_line1="Address",
            city="City",
            state="State",
            postal_code="12345",
            country="Brazil"
        )
        
        # Tentar criar outro que excede 100%
        new_ubo_data = {
            'kyc_profile': kyc_profile.id,
            'full_name': 'New UBO',
            'date_of_birth': '1985-01-01',
            'nationality': 'Brazilian',
            'ownership_percentage': '50.00',
            'address_line1': 'New Address',
            'city': 'City',
            'state': 'State',
            'postal_code': '12345',
            'country': 'Brazil'
        }
        
        url = reverse('kyc:ubodeclaration-list')
        response = authenticated_client.post(url, new_ubo_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.api
@pytest.mark.views
class TestKYCDocumentViewSet:
    """Testes para KYCDocumentViewSet"""
    
    def test_list_documents_user_filter(self, authenticated_client, kyc_profile):
        """Teste filtro de documentos por usuário"""
        # Criar documento do usuário
        doc1 = KYCDocument.objects.create(
            kyc_profile=kyc_profile,
            document_type='passport',
            original_filename='passport.pdf',
            file_size=1024,
            mime_type='application/pdf'
        )
        
        # Criar outro usuário e documento
        other_user = User.objects.create_user(username='other', email='other@test.com')
        other_profile = KYCProfile.objects.create(user=other_user, full_name='Other User')
        doc2 = KYCDocument.objects.create(
            kyc_profile=other_profile,
            document_type='utility_bill',
            original_filename='bill.pdf',
            file_size=1024,
            mime_type='application/pdf'
        )
        
        url = reverse('kyc:kycdocument-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == doc1.id
    
    def test_process_ocr_endpoint(self, authenticated_client, kyc_profile):
        """Teste endpoint de processamento OCR"""
        document = KYCDocument.objects.create(
            kyc_profile=kyc_profile,
            document_type='passport',
            original_filename='passport.pdf',
            file_size=1024,
            mime_type='application/pdf'
        )
        
        url = reverse('kyc:kycdocument-process-ocr', kwargs={'pk': document.id})
        response = authenticated_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        document.refresh_from_db()
        assert document.ocr_processed is True
