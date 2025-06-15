"""
Serializers do app KYC
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import KYCProfile, UBODeclaration, PEPDeclaration, KYCDocument


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para usuário"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class UBODeclarationSerializer(serializers.ModelSerializer):
    """Serializer para declarações UBO"""
    
    class Meta:
        model = UBODeclaration
        fields = [
            'id', 'kyc_profile', 'full_name', 'date_of_birth', 'nationality',
            'ownership_percentage', 'address_line1', 'address_line2', 'city',
            'state', 'postal_code', 'country', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_ownership_percentage(self, value):
        """Validar percentual de propriedade"""
        if value < 0 or value > 100:
            raise serializers.ValidationError(_('Ownership percentage must be between 0 and 100'))
        return value
    
    def validate(self, data):
        """Validação geral"""
        # Validar se o total não excede 100%
        kyc_profile = data.get('kyc_profile')
        ownership_percentage = data.get('ownership_percentage')
        
        if kyc_profile and ownership_percentage:
            existing_ubos = UBODeclaration.objects.filter(kyc_profile=kyc_profile)
            if self.instance:
                existing_ubos = existing_ubos.exclude(id=self.instance.id)
            
            total_existing = sum(ubo.ownership_percentage for ubo in existing_ubos)
            
            if total_existing + ownership_percentage > 100:
                raise serializers.ValidationError({
                    'ownership_percentage': _('Total ownership percentage cannot exceed 100%')
                })
        
        return data


class PEPDeclarationSerializer(serializers.ModelSerializer):
    """Serializer para declarações PEP"""
    
    class Meta:
        model = PEPDeclaration
        fields = [
            'id', 'kyc_profile', 'is_pep', 'pep_type', 'position_held',
            'organization', 'country', 'start_date', 'end_date',
            'related_pep_name', 'relationship_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validação para PEP"""
        is_pep = data.get('is_pep', False)
        
        if is_pep:
            # Se é PEP, campos obrigatórios
            required_fields = ['pep_type', 'position_held', 'organization']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({
                        field: _('This field is required for PEP declarations')
                    })
        
        # Validar datas
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                'end_date': _('End date must be after start date')
            })
        
        return data


class KYCDocumentSerializer(serializers.ModelSerializer):
    """Serializer para documentos KYC"""
    
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = KYCDocument
        fields = [
            'id', 'kyc_profile', 'document_type', 'file', 'file_url',
            'original_filename', 'file_size', 'mime_type', 'ocr_processed',
            'ocr_text', 'ocr_confidence', 'is_verified', 'verification_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'file_size', 'mime_type', 'ocr_processed', 'ocr_text',
            'ocr_confidence', 'created_at', 'updated_at'
        ]
    
    def get_file_url(self, obj):
        """Obter URL do arquivo"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def validate_file(self, value):
        """Validar arquivo"""
        # Validar tamanho (10MB max)
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError(_('File size cannot exceed 10MB'))
        
        # Validar tipo de arquivo
        allowed_types = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'image/gif',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(_('File type not allowed'))
        
        return value
    
    def create(self, validated_data):
        """Criar documento com metadados"""
        file = validated_data['file']
        validated_data['original_filename'] = file.name
        validated_data['file_size'] = file.size
        validated_data['mime_type'] = file.content_type
        
        return super().create(validated_data)


class KYCProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil KYC"""
    
    user = UserSerializer(read_only=True)
    ubo_declarations = UBODeclarationSerializer(many=True, read_only=True)
    pep_declarations = PEPDeclarationSerializer(many=True, read_only=True)
    documents = KYCDocumentSerializer(many=True, read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    
    # Campos calculados
    completion_percentage = serializers.SerializerMethodField()
    ubo_validation_status = serializers.SerializerMethodField()
    
    class Meta:
        model = KYCProfile
        fields = [
            'id', 'user', 'status', 'full_name', 'date_of_birth', 'nationality',
            'document_number', 'document_type', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'occupation', 'employer',
            'annual_income', 'source_of_funds', 'created_at', 'updated_at',
            'reviewed_by', 'reviewed_at', 'notes', 'ubo_declarations',
            'pep_declarations', 'documents', 'completion_percentage',
            'ubo_validation_status'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at', 'reviewed_by',
            'reviewed_at', 'completion_percentage', 'ubo_validation_status'
        ]
    
    def get_completion_percentage(self, obj):
        """Calcular percentual de completude"""
        required_fields = [
            'full_name', 'date_of_birth', 'nationality', 'document_number',
            'document_type', 'address_line1', 'city', 'state', 'postal_code',
            'country', 'occupation', 'source_of_funds'
        ]
        
        completed_fields = 0
        for field in required_fields:
            if getattr(obj, field):
                completed_fields += 1
        
        # Verificar documentos obrigatórios
        required_docs = ['passport', 'utility_bill']
        uploaded_docs = obj.documents.values_list('document_type', flat=True)
        docs_complete = all(doc in uploaded_docs for doc in required_docs)
        
        # Verificar UBO
        ubo_validation = UBODeclaration.validate_ubo_declarations(obj)
        ubo_complete = ubo_validation['is_valid']
        
        # Verificar PEP
        pep_complete = obj.pep_declarations.exists()
        
        # Calcular percentual
        base_percentage = (completed_fields / len(required_fields)) * 70  # 70% para campos básicos
        doc_percentage = 15 if docs_complete else 0  # 15% para documentos
        ubo_percentage = 10 if ubo_complete else 0   # 10% para UBO
        pep_percentage = 5 if pep_complete else 0    # 5% para PEP
        
        return min(100, base_percentage + doc_percentage + ubo_percentage + pep_percentage)
    
    def get_ubo_validation_status(self, obj):
        """Obter status de validação UBO"""
        return UBODeclaration.validate_ubo_declarations(obj)
    
    def validate_annual_income(self, value):
        """Validar renda anual"""
        if value is not None and value < 0:
            raise serializers.ValidationError(_('Annual income cannot be negative'))
        return value
    
    def validate(self, data):
        """Validação geral do perfil"""
        # Validar se o usuário pode editar este perfil
        request = self.context.get('request')
        if request and not request.user.is_staff:
            if self.instance and self.instance.user != request.user:
                raise serializers.ValidationError(_('Cannot edit other users profiles'))
        
        return data

