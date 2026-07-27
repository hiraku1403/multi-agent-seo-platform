document.getElementById('generateBtn').addEventListener('click', async () => {
    const topic = document.getElementById('topicInput').value.trim();
    
    if (!topic) {
        alert('Por favor, digite um tópico!');
        return;
    }
    
    // Mostra loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('generateBtn').disabled = true;
    
    try {
        // 🔥 CORREÇÃO: Remover /api/ do caminho
        const response = await fetch('/generate-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic })
        });
        
        // Verificar se a resposta é JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            console.error('Resposta não é JSON:', text);
            throw new Error('Erro: A resposta do servidor não é JSON. Verifique a API.');
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Mostra resultados
            document.getElementById('researchResult').textContent = data.research || 'N/A';
            document.getElementById('seoResult').textContent = data.seo_analysis || 'N/A';
            
            // Processa o artigo
            const articleContent = data.final_article || data.article || '';
            document.getElementById('articleResult').innerHTML = articleContent
                .split('\n')
                .map(line => {
                    if (line.startsWith('# ')) return `<h1>${line.substring(2)}</h1>`;
                    if (line.startsWith('## ')) return `<h2>${line.substring(3)}</h2>`;
                    if (line.startsWith('### ')) return `<h3>${line.substring(4)}</h3>`;
                    if (line.trim() === '') return '<br>';
                    return `<p>${line}</p>`;
                })
                .join('');
            
            document.getElementById('results').classList.remove('hidden');
        } else {
            alert('Erro ao gerar conteúdo: ' + (data.error || 'Erro desconhecido'));
        }
    } catch (error) {
        console.error('Erro completo:', error);
        alert('Erro: ' + error.message + '\n\nVerifique o console para mais detalhes.');
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('generateBtn').disabled = false;
    }
});

// Enter key para pesquisar
document.getElementById('topicInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('generateBtn').click();
    }
});

// Função para testar a API
async function testAPI() {
    try {
        const response = await fetch('/');
        const data = await response.json();
        console.log('API Status:', data);
        return data;
    } catch (error) {
        console.error('Erro ao testar API:', error);
        return null;
    }
}

// Testar API quando a página carregar
document.addEventListener('DOMContentLoaded', async () => {
    const status = await testAPI();
    if (status && status.status === 'online') {
        console.log('✅ API está online!');
    } else {
        console.warn('⚠️ API pode estar offline. Verifique o console.');
    }
});