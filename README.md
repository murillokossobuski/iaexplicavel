# iaexplicavel
projeto de iniciação científica na utfpr com o tema "ia explicável na astronomia"

## Buscador de Óculos Zerezes

Este repositório também contém um script para encontrar os óculos mais baratos da Zerezes.

### Uso

O script `find_cheapest_glasses.py` pode ser executado de três formas:

#### 1. Modo de demonstração (recomendado para testes)
```bash
python3 find_cheapest_glasses.py --demo
```

#### 2. Com arquivo JSON personalizado
```bash
python3 find_cheapest_glasses.py --data seu_arquivo.json
```

Formato do arquivo JSON:
```json
[
  {
    "name": "Nome do Produto",
    "price": 99.90,
    "url": "https://www.zerezes.com.br/produto/exemplo"
  }
]
```

#### 3. Web scraping (requer acesso ao site)
```bash
python3 find_cheapest_glasses.py
```

### Exemplo de saída

```
======================================================================
🏆 ÓCULOS MAIS BARATO:
======================================================================
  📝 Nome: Óculos de Leitura +2.00
  💰 Preço: R$ 39.90
  🔗 Link: https://www.zerezes.com.br/produto/leitura-200
======================================================================
```

### Requisitos

- Python 3.x
- requests (instale com `pip install requests`)
- beautifulsoup4 (opcional, para web scraping - instale com `pip install beautifulsoup4`)

### Instalação de dependências

Para habilitar todas as funcionalidades:
```bash
pip install requests beautifulsoup4
```

