document.getElementById('generateBtn').addEventListener('click', async () => {
    const topic = document.getElementById('topicInput').value.trim();
    
    if (!topic) {
        alert('Por favor, digite um tópico!');
        return;
    }
    
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('generateBtn').disabled = true;
    
    try {
        // 1. Envia a solicitação de geração
        const response = await fetch('/api/generate-content', {
            method: 'POST',  
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic })
        });
        
        const initData = await response.json();
        const jobId = initData.job_id;
        
        // 2. Cria uma função de checagem periódica
        const checkStatus = setInterval(async () => {
            try {
                const statusResponse = await fetch(`/api/job/${jobId}`);
                const data = await statusResponse.json();
                
                if (data.status === 'completed') {
                    clearInterval(checkStatus); // Para de perguntar
                    
                    if (data.success) {
                        // Mostra os resultados na tela
                        document.getElementById('researchResult').textContent = data.research || 'N/A';
                        document.getElementById('seoResult').textContent = data.seo_analysis || 'N/A';
                        
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
                        alert('Erro ao gerar conteúdo: ' + (data.error || 'Erro desconhecido nos agentes'));
                    }
                    
                    document.getElementById('loading').classList.add('hidden');
                    document.getElementById('generateBtn').disabled = false;
                }
            } catch (err) {
                clearInterval(checkStatus);
                console.error(err);
                document.getElementById('loading').classList.add('hidden');
                document.getElementById('generateBtn').disabled = false;
            }
        }, 25000 ); // Pergunta a cada 5 segundos
        
    } catch (error) {
        console.error('Erro completo:', error);
        alert('Erro: ' + error.message);
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
        const response = await fetch('/api/health'); //  Correto
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
    if (status && status.status === 'healthy')  {
        console.log('✅ API está online!');
    } else {
        console.warn('⚠️ API pode estar offline. Verifique o console.');
    }
});