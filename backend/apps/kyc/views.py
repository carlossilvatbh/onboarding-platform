"""
Views do app KYC com correções de bugs identificados
CORREÇÃO: Implementação de paginação para tabela PEPs
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
import logging

from .models import KYCProfile, UBODeclaration, PEPDeclaration, KYCDocument
from .serializers import (
    KYCProfileSerializer, 
    UBODeclarationSerializer, 
    PEPDeclarationSerializer,
    KYCDocumentSerializer
)

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão para o projeto"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargePEPResultsSetPagination(PageNumberPagination):
    """
    CORREÇÃO: Paginação específica para tabela PEPs
    Resolve problema de congelamento com listas grandes
    """
    page_size = 10  # Menor para melhor performance
    page_size_query_param = 'page_size'
    max_page_size = 50  # Limite menor para evitar sobrecarga


class KYCProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para perfis KYC"""
    
    queryset = KYCProfile.objects.all()
    serializer_class = KYCProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'nationality', 'country']
    search_fields = ['full_name', 'document_number', 'user__email']
    ordering_fields = ['created_at', 'updated_at', 'full_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrar por usuário se não for staff"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, pk=None):
        """Submeter perfil para revisão"""
        profile = self.get_object()
        
        if profile.status != 'pending':
            return Response(
                {'error': _('Profile can only be submitted when in pending status')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar se tem documentos necessários
        required_docs = ['passport', 'utility_bill']
        uploaded_docs = profile.documents.values_list('document_type', flat=True)
        
        missing_docs = [doc for doc in required_docs if doc not in uploaded_docs]
        if missing_docs:
            return Response(
                {'error': _('Missing required documents'), 'missing': missing_docs},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile.status = 'in_review'
        profile.save()
        
        return Response({'message': _('Profile submitted for review successfully')})
    
    @action(detail=True, methods=['get'])
    def validation_status(self, request, pk=None):
        """
        CORREÇÃO: Endpoint seguro para validação UBO
        Trata casos onde beneficiário não é declarado
        """
        profile = self.get_object()
        
        try:
            # Usar método seguro para validação UBO
            ubo_validation = UBODeclaration.validate_ubo_declarations(profile)
            
            # Validar documentos
            required_docs = ['passport', 'utility_bill']
            uploaded_docs = list(profile.documents.values_list('document_type', flat=True))
            missing_docs = [doc for doc in required_docs if doc not in uploaded_docs]
            
            # Validar PEP
            pep_declaration = profile.pep_declarations.first()
            pep_complete = pep_declaration is not None
            
            validation_result = {
                'ubo_validation': ubo_validation,
                'documents': {
                    'required': required_docs,
                    'uploaded': uploaded_docs,
                    'missing': missing_docs,
                    'complete': len(missing_docs) == 0
                },
                'pep_declaration': {
                    'complete': pep_complete,
                    'is_pep': pep_declaration.is_pep if pep_declaration else False
                },
                'overall_complete': (
                    ubo_validation['is_valid'] and 
                    len(missing_docs) == 0 and 
                    pep_complete
                )
            }
            
            return Response(validation_result)
            
        except Exception as e:
            logger.error(f"Erro na validação do perfil {pk}: {str(e)}")
            return Response(
                {'error': _('Error validating profile. Please try again.')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UBODeclarationViewSet(viewsets.ModelViewSet):
    """ViewSet para declarações UBO"""
    
    serializer_class = UBODeclarationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['kyc_profile', 'nationality', 'country']
    ordering_fields = ['ownership_percentage', 'created_at']
    ordering = ['-ownership_percentage']
    
    def get_queryset(self):
        """Filtrar UBOs baseado no perfil KYC do usuário"""
        if self.request.user.is_staff:
            return UBODeclaration.objects.all()
        
        # Usuários normais só veem seus próprios UBOs
        user_profiles = KYCProfile.objects.filter(user=self.request.user)
        return UBODeclaration.objects.filter(kyc_profile__in=user_profiles)
    
    def perform_create(self, serializer):
        """Validar ownership ao criar UBO"""
        kyc_profile = serializer.validated_data['kyc_profile']
        
        # Verificar se o usuário pode criar UBO para este perfil
        if not self.request.user.is_staff and kyc_profile.user != self.request.user:
            raise PermissionError(_('Cannot create UBO for other users'))
        
        # Validar percentual total
        existing_ubos = UBODeclaration.objects.filter(kyc_profile=kyc_profile)
        total_existing = sum(ubo.ownership_percentage for ubo in existing_ubos)
        new_percentage = serializer.validated_data['ownership_percentage']
        
        if total_existing + new_percentage > 100:
            raise ValidationError(_('Total ownership percentage would exceed 100%'))
        
        serializer.save()


class PEPDeclarationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para declarações PEP
    CORREÇÃO: Implementação de paginação otimizada para evitar congelamento
    """
    
    serializer_class = PEPDeclarationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LargePEPResultsSetPagination  # Paginação específica
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_pep', 'pep_type', 'country']
    search_fields = ['position_held', 'organization', 'related_pep_name']
    ordering_fields = ['created_at', 'start_date', 'end_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        CORREÇÃO: Queryset otimizado para performance
        Evita carregar todos os registros de uma vez
        """
        queryset = PEPDeclaration.objects.select_related('kyc_profile', 'kyc_profile__user')
        
        if not self.request.user.is_staff:
            # Filtrar apenas PEPs do usuário atual
            queryset = queryset.filter(kyc_profile__user=self.request.user)
        
        # Aplicar filtros de busca se fornecidos
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(position_held__icontains=search) |
                Q(organization__icontains=search) |
                Q(related_pep_name__icontains=search) |
                Q(kyc_profile__full_name__icontains=search)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        CORREÇÃO: List override com logging para monitoramento
        """
        try:
            logger.info(f"PEP list request from user {request.user.id}")
            response = super().list(request, *args, **kwargs)
            logger.info(f"PEP list response: {len(response.data.get('results', []))} items")
            return response
        except Exception as e:
            logger.error(f"Erro na listagem PEP: {str(e)}")
            return Response(
                {'error': _('Error loading PEP declarations')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        CORREÇÃO: Endpoint de resumo otimizado
        Evita carregar dados desnecessários
        """
        try:
            queryset = self.get_queryset()
            
            summary_data = {
                'total_declarations': queryset.count(),
                'pep_count': queryset.filter(is_pep=True).count(),
                'non_pep_count': queryset.filter(is_pep=False).count(),
                'by_type': {}
            }
            
            # Contar por tipo (apenas se necessário)
            if summary_data['pep_count'] > 0:
                for pep_type, _ in PEPDeclaration.PEP_TYPES:
                    count = queryset.filter(is_pep=True, pep_type=pep_type).count()
                    if count > 0:
                        summary_data['by_type'][pep_type] = count
            
            return Response(summary_data)
            
        except Exception as e:
            logger.error(f"Erro no resumo PEP: {str(e)}")
            return Response(
                {'error': _('Error generating PEP summary')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class KYCDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet para documentos KYC"""
    
    serializer_class = KYCDocumentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document_type', 'is_verified', 'ocr_processed']
    ordering_fields = ['created_at', 'file_size']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrar documentos baseado no perfil KYC do usuário"""
        if self.request.user.is_staff:
            return KYCDocument.objects.all()
        
        # Usuários normais só veem seus próprios documentos
        user_profiles = KYCProfile.objects.filter(user=self.request.user)
        return KYCDocument.objects.filter(kyc_profile__in=user_profiles)
    
    @action(detail=True, methods=['post'])
    def process_ocr(self, request, pk=None):
        """Processar OCR do documento"""
        document = self.get_object()
        
        try:
            # Aqui seria implementada a lógica de OCR
            # Por enquanto, simulamos o processamento
            document.ocr_processed = True
            document.ocr_text = "OCR processing completed"
            document.ocr_confidence = 0.95
            document.save()
            
            return Response({'message': _('OCR processing completed successfully')})
            
        except Exception as e:
            logger.error(f"Erro no processamento OCR do documento {pk}: {str(e)}")
            return Response(
                {'error': _('Error processing OCR')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

