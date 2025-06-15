"""
Comando Django para verificar status das traduções
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import re


class Command(BaseCommand):
    help = 'Verifica o status das traduções do projeto'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Verificar apenas um idioma específico (en, pt_BR)',
        )
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Mostrar informações detalhadas',
        )
        parser.add_argument(
            '--missing',
            action='store_true',
            help='Mostrar apenas strings não traduzidas',
        )
    
    def handle(self, *args, **options):
        """Executar verificação das traduções"""
        
        self.stdout.write(
            self.style.SUCCESS('🌍 Verificando traduções do projeto ONBOARDING...\n')
        )
        
        # Idiomas suportados
        languages = ['en', 'pt_BR']
        
        if options['language']:
            if options['language'] in languages:
                languages = [options['language']]
            else:
                raise CommandError(f'Idioma não suportado: {options["language"]}')
        
        # Verificar cada idioma
        for lang in languages:
            self.check_language(lang, options)
    
    def check_language(self, language, options):
        """Verificar traduções de um idioma específico"""
        
        po_file = os.path.join(
            settings.BASE_DIR, 
            'locale', 
            language, 
            'LC_MESSAGES', 
            'django.po'
        )
        
        if not os.path.exists(po_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Arquivo não encontrado: {po_file}')
            )
            return
        
        self.stdout.write(f'🔍 Verificando {language}...')
        
        # Ler arquivo .po
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extrair estatísticas
        stats = self.extract_stats(content)
        
        # Mostrar estatísticas
        self.show_stats(language, stats, options)
        
        # Mostrar strings não traduzidas se solicitado
        if options['missing']:
            self.show_missing_translations(content, language)
    
    def extract_stats(self, content):
        """Extrair estatísticas do arquivo .po"""
        
        # Padrões regex
        msgid_pattern = re.compile(r'^msgid\s+"(.+)"', re.MULTILINE)
        msgstr_pattern = re.compile(r'^msgstr\s+"(.+)"', re.MULTILINE)
        fuzzy_pattern = re.compile(r'^#,.*fuzzy', re.MULTILINE)
        
        # Contar ocorrências
        msgids = msgid_pattern.findall(content)
        msgstrs = msgstr_pattern.findall(content)
        fuzzy_count = len(fuzzy_pattern.findall(content))
        
        # Filtrar strings vazias
        total_strings = len([m for m in msgids if m.strip()])
        translated_strings = len([m for m in msgstrs if m.strip()])
        empty_strings = total_strings - translated_strings
        
        return {
            'total': total_strings,
            'translated': translated_strings,
            'empty': empty_strings,
            'fuzzy': fuzzy_count,
            'percentage': (translated_strings * 100 // total_strings) if total_strings > 0 else 0
        }
    
    def show_stats(self, language, stats, options):
        """Mostrar estatísticas formatadas"""
        
        # Nome do idioma
        lang_names = {
            'en': 'English',
            'pt_BR': 'Português Brasileiro'
        }
        
        lang_name = lang_names.get(language, language)
        
        self.stdout.write(f'\n📊 {lang_name} ({language}):')
        self.stdout.write(f'   📝 Total de strings: {stats["total"]}')
        
        # Colorir baseado na porcentagem
        if stats['percentage'] >= 90:
            color = self.style.SUCCESS
        elif stats['percentage'] >= 70:
            color = self.style.WARNING
        else:
            color = self.style.ERROR
        
        self.stdout.write(
            f'   ✅ Traduzidas: {color(str(stats["translated"]))} ({stats["percentage"]}%)'
        )
        
        if stats['empty'] > 0:
            self.stdout.write(
                f'   ❌ Não traduzidas: {self.style.ERROR(str(stats["empty"]))}'
            )
        
        if stats['fuzzy'] > 0:
            self.stdout.write(
                f'   ⚠️ Fuzzy: {self.style.WARNING(str(stats["fuzzy"]))}'
            )
        
        # Barra de progresso
        if options['detailed']:
            self.show_progress_bar(stats['percentage'])
        
        self.stdout.write('')
    
    def show_progress_bar(self, percentage):
        """Mostrar barra de progresso"""
        
        bar_length = 20
        filled_length = int(bar_length * percentage // 100)
        
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        self.stdout.write(f'   [{bar}] {percentage}%')
    
    def show_missing_translations(self, content, language):
        """Mostrar strings não traduzidas"""
        
        self.stdout.write(f'\n🔍 Strings não traduzidas em {language}:')
        
        # Dividir em blocos msgid/msgstr
        blocks = re.split(r'\n\n+', content)
        
        missing_count = 0
        for block in blocks:
            if 'msgid' in block and 'msgstr' in block:
                # Extrair msgid e msgstr
                msgid_match = re.search(r'msgid\s+"(.+)"', block)
                msgstr_match = re.search(r'msgstr\s+"(.+)"', block)
                
                if msgid_match and msgstr_match:
                    msgid = msgid_match.group(1)
                    msgstr = msgstr_match.group(1)
                    
                    # Verificar se não está traduzido
                    if msgid.strip() and not msgstr.strip():
                        missing_count += 1
                        self.stdout.write(f'   {missing_count}. "{msgid}"')
        
        if missing_count == 0:
            self.stdout.write(
                self.style.SUCCESS('   ✅ Todas as strings estão traduzidas!')
            )
        else:
            self.stdout.write(f'\n   Total não traduzidas: {missing_count}')
        
        self.stdout.write('')

