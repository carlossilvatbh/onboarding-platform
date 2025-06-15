"""
Models para o app KYC (Know Your Customer)
Inclui correções para bugs identificados no relatório
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


class KYCProfile(models.Model):
    """Perfil KYC do usuário"""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_review', _('In Review')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('requires_update', _('Requires Update')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kyc_profile')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Dados pessoais
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    document_number = models.CharField(max_length=50)
    document_type = models.CharField(max_length=20)
    
    # Endereço
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Informações financeiras
    occupation = models.CharField(max_length=255)
    employer = models.CharField(max_length=255, blank=True)
    annual_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    source_of_funds = models.TextField()
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_kyc_profiles'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('KYC Profile')
        verbose_name_plural = _('KYC Profiles')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"KYC Profile - {self.full_name} ({self.status})"


class UBODeclaration(models.Model):
    """
    Declaração de Beneficiário Final (Ultimate Beneficial Owner)
    CORREÇÃO: Tratamento adequado para casos onde beneficiário não é declarado
    """
    
    kyc_profile = models.ForeignKey(KYCProfile, on_delete=models.CASCADE, related_name='ubo_declarations')
    
    # Informações do UBO
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    ownership_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Endereço do UBO
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('UBO Declaration')
        verbose_name_plural = _('UBO Declarations')
        ordering = ['-ownership_percentage']
    
    def __str__(self):
        return f"UBO: {self.full_name} ({self.ownership_percentage}%)"
    
    @classmethod
    def get_ubos_for_profile(cls, kyc_profile):
        """
        CORREÇÃO: Método seguro para obter UBOs de um perfil
        Trata casos onde não há UBOs declarados
        """
        try:
            ubos = cls.objects.filter(kyc_profile=kyc_profile)
            return list(ubos) if ubos.exists() else []
        except Exception as e:
            # Log do erro para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao buscar UBOs para perfil {kyc_profile.id}: {str(e)}")
            return []
    
    @classmethod
    def validate_ubo_declarations(cls, kyc_profile):
        """
        CORREÇÃO: Validação robusta de declarações UBO
        Evita TypeError quando beneficiário não é declarado
        """
        try:
            ubos = cls.get_ubos_for_profile(kyc_profile)
            
            if not ubos:
                # Caso não haja UBOs declarados, retorna validação específica
                return {
                    'is_valid': False,
                    'errors': [_('No UBO declarations found. At least one UBO must be declared.')],
                    'total_percentage': 0
                }
            
            total_percentage = sum(ubo.ownership_percentage for ubo in ubos)
            errors = []
            
            # Validações
            if total_percentage > 100:
                errors.append(_('Total ownership percentage cannot exceed 100%'))
            
            if total_percentage < 25:
                errors.append(_('At least 25% ownership must be declared for UBO requirements'))
            
            # Validar cada UBO individualmente
            for ubo in ubos:
                if ubo.ownership_percentage < 0:
                    errors.append(f_('Invalid ownership percentage for {ubo.full_name}'))
                
                if not ubo.full_name.strip():
                    errors.append(_('UBO name cannot be empty'))
            
            return {
                'is_valid': len(errors) == 0,
                'errors': errors,
                'total_percentage': total_percentage,
                'ubo_count': len(ubos)
            }
            
        except Exception as e:
            # Log do erro e retorna validação com erro
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro na validação UBO para perfil {kyc_profile.id}: {str(e)}")
            
            return {
                'is_valid': False,
                'errors': [_('Error validating UBO declarations. Please try again.')],
                'total_percentage': 0
            }


class PEPDeclaration(models.Model):
    """
    Declaração de Pessoa Politicamente Exposta (PEP)
    """
    
    PEP_TYPES = [
        ('domestic', _('Domestic PEP')),
        ('foreign', _('Foreign PEP')),
        ('international', _('International Organization PEP')),
        ('family', _('Family Member of PEP')),
        ('close_associate', _('Close Associate of PEP')),
    ]
    
    kyc_profile = models.ForeignKey(KYCProfile, on_delete=models.CASCADE, related_name='pep_declarations')
    
    is_pep = models.BooleanField(default=False)
    pep_type = models.CharField(max_length=20, choices=PEP_TYPES, blank=True)
    position_held = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # Relacionamento com PEP (se aplicável)
    related_pep_name = models.CharField(max_length=255, blank=True)
    relationship_type = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('PEP Declaration')
        verbose_name_plural = _('PEP Declarations')
        ordering = ['-created_at']
    
    def __str__(self):
        if self.is_pep:
            return f"PEP: {self.kyc_profile.full_name} - {self.position_held}"
        return f"Non-PEP: {self.kyc_profile.full_name}"


class KYCDocument(models.Model):
    """Documentos anexados ao processo KYC"""
    
    DOCUMENT_TYPES = [
        ('passport', _('Passport')),
        ('national_id', _('National ID')),
        ('drivers_license', _('Driver\'s License')),
        ('utility_bill', _('Utility Bill')),
        ('bank_statement', _('Bank Statement')),
        ('proof_of_income', _('Proof of Income')),
        ('other', _('Other')),
    ]
    
    kyc_profile = models.ForeignKey(KYCProfile, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='kyc_documents/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=100)
    
    # OCR e processamento
    ocr_processed = models.BooleanField(default=False)
    ocr_text = models.TextField(blank=True)
    ocr_confidence = models.FloatField(null=True, blank=True)
    
    # Validação
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('KYC Document')
        verbose_name_plural = _('KYC Documents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.kyc_profile.full_name}"

