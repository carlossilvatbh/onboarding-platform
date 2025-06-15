#!/bin/bash

# Script para gerenciar traduções do projeto ONBOARDING

echo "🌍 Gerenciando traduções do projeto ONBOARDING..."

# Navegar para o diretório backend
cd backend

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️ Ambiente virtual não detectado. Ativando..."
    source ../venv/bin/activate
fi

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  extract    - Extrair strings para tradução"
    echo "  compile    - Compilar traduções"
    echo "  update     - Atualizar arquivos de tradução existentes"
    echo "  check      - Verificar traduções"
    echo "  stats      - Mostrar estatísticas de tradução"
    echo "  help       - Mostrar esta ajuda"
    echo ""
}

# Função para extrair strings
extract_strings() {
    echo "📝 Extraindo strings para tradução..."
    
    # Criar diretórios se não existirem
    mkdir -p locale/en/LC_MESSAGES
    mkdir -p locale/pt_BR/LC_MESSAGES
    
    # Extrair strings do Django
    python manage.py makemessages -l en -l pt_BR --ignore=venv --ignore=node_modules
    
    echo "✅ Strings extraídas com sucesso!"
}

# Função para compilar traduções
compile_translations() {
    echo "🔨 Compilando traduções..."
    
    python manage.py compilemessages
    
    echo "✅ Traduções compiladas com sucesso!"
}

# Função para atualizar traduções
update_translations() {
    echo "🔄 Atualizando traduções existentes..."
    
    python manage.py makemessages -l en -l pt_BR --ignore=venv --ignore=node_modules --no-obsolete
    
    echo "✅ Traduções atualizadas com sucesso!"
}

# Função para verificar traduções
check_translations() {
    echo "🔍 Verificando traduções..."
    
    # Verificar arquivos .po
    for lang in en pt_BR; do
        po_file="locale/$lang/LC_MESSAGES/django.po"
        if [ -f "$po_file" ]; then
            echo "📄 Verificando $lang..."
            
            # Contar strings traduzidas e não traduzidas
            total=$(grep -c "^msgid" "$po_file")
            translated=$(grep -c "^msgstr \"[^\"]\+\"" "$po_file")
            untranslated=$((total - translated))
            
            if [ $total -gt 0 ]; then
                percentage=$((translated * 100 / total))
                echo "   Total: $total strings"
                echo "   Traduzidas: $translated ($percentage%)"
                echo "   Não traduzidas: $untranslated"
            fi
            
            # Verificar sintaxe
            if msgfmt --check "$po_file" 2>/dev/null; then
                echo "   ✅ Sintaxe OK"
            else
                echo "   ❌ Erro de sintaxe"
            fi
        else
            echo "❌ Arquivo $po_file não encontrado"
        fi
        echo ""
    done
}

# Função para mostrar estatísticas
show_stats() {
    echo "📊 Estatísticas de tradução:"
    echo ""
    
    for lang in en pt_BR; do
        po_file="locale/$lang/LC_MESSAGES/django.po"
        if [ -f "$po_file" ]; then
            echo "🌍 $lang:"
            
            # Estatísticas detalhadas
            total=$(grep -c "^msgid" "$po_file")
            translated=$(grep -c "^msgstr \"[^\"]\+\"" "$po_file")
            empty=$(grep -c "^msgstr \"\"$" "$po_file")
            fuzzy=$(grep -c "#, fuzzy" "$po_file")
            
            if [ $total -gt 0 ]; then
                percentage=$((translated * 100 / total))
                echo "   📝 Total de strings: $total"
                echo "   ✅ Traduzidas: $translated ($percentage%)"
                echo "   ❌ Vazias: $empty"
                echo "   ⚠️ Fuzzy: $fuzzy"
                
                # Barra de progresso simples
                filled=$((percentage / 5))
                empty_bars=$((20 - filled))
                printf "   ["
                for ((i=1; i<=filled; i++)); do printf "█"; done
                for ((i=1; i<=empty_bars; i++)); do printf "░"; done
                printf "] %d%%\n" $percentage
            fi
        fi
        echo ""
    done
}

# Processar argumentos
case "${1:-help}" in
    extract)
        extract_strings
        ;;
    compile)
        compile_translations
        ;;
    update)
        update_translations
        ;;
    check)
        check_translations
        ;;
    stats)
        show_stats
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Comando desconhecido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

# Voltar ao diretório raiz
cd ..

