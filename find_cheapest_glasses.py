#!/usr/bin/env python3
"""
Script to find the cheapest glasses from Zerezes

This script can work in three modes:
1. Web scraping mode (requires internet access to zerezes.com.br)
2. Manual data mode (using a JSON file with product data)
3. Demo mode (using sample data for testing)

Usage:
    python3 find_cheapest_glasses.py                    # Try web scraping
    python3 find_cheapest_glasses.py --data products.json  # Use JSON file
    python3 find_cheapest_glasses.py --demo               # Use demo data
"""

import requests
from typing import Dict, List, Optional
import json
import sys
import argparse
import os

def fetch_zerezes_products() -> Optional[List[Dict]]:
    """
    Fetch product data from Zerezes website
    
    Returns:
        List of product dictionaries or None if fetch fails
    """
    # Try different possible URLs for Zerezes
    possible_urls = [
        "https://www.zerezes.com.br",
        "https://zerezes.com.br",
        "https://www.zerezes.com",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in possible_urls:
        try:
            print(f"Tentando acessar: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✓ Conectado com sucesso a {url}")
                return parse_products(response.text)
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro ao acessar {url}: {e}")
            continue
    
    return None

def parse_products(html_content: str) -> List[Dict]:
    """
    Parse HTML content to extract product information
    
    Args:
        html_content: HTML string from the website
        
    Returns:
        List of product dictionaries
    """
    products = []
    
    try:
        # Try to parse HTML with BeautifulSoup if available
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for product containers (this would need to be adjusted based on actual site structure)
        product_elements = soup.find_all(class_=['product', 'item', 'product-item'])
        
        for element in product_elements:
            try:
                # Extract product information
                name_elem = element.find(class_=['product-name', 'title', 'name'])
                price_elem = element.find(class_=['price', 'product-price'])
                link_elem = element.find('a')
                
                if name_elem and price_elem:
                    # Clean up price - handle Brazilian number format (e.g., R$ 1.234,56)
                    price_text = price_elem.get_text().strip()
                    # Remove currency symbol and spaces
                    price_text = price_text.replace('R$', '').strip()
                    
                    # Handle Brazilian format: thousands separator is dot, decimal is comma
                    # Remove thousand separators (dots) but keep the last part after comma
                    if ',' in price_text:
                        # Split by comma to separate integer and decimal parts
                        parts = price_text.split(',')
                        if len(parts) == 2:
                            # Remove dots from integer part, keep decimal part
                            integer_part = parts[0].replace('.', '')
                            decimal_part = parts[1]
                            price_text = f"{integer_part}.{decimal_part}"
                    else:
                        # No comma, just remove dots (in case it's a format like 1234.00)
                        price_text = price_text.replace('.', '')
                    
                    try:
                        price = float(price_text)
                        product = {
                            'name': name_elem.get_text().strip(),
                            'price': price,
                            'url': link_elem.get('href', '') if link_elem else ''
                        }
                        products.append(product)
                    except ValueError:
                        continue
            except Exception as e:
                continue
                
    except ImportError:
        print("⚠ BeautifulSoup não está instalado. Instale com: pip install beautifulsoup4")
        return []
    except Exception as e:
        print(f"⚠ Erro ao processar HTML: {e}")
        return []
    
    return products

def load_products_from_json(filepath: str) -> Optional[List[Dict]]:
    """
    Load product data from a JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        List of product dictionaries or None if load fails
    """
    try:
        if not os.path.exists(filepath):
            print(f"✗ Arquivo não encontrado: {filepath}")
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'products' in data:
            return data['products']
        else:
            print("✗ Formato de JSON inválido. Esperado: lista de produtos ou objeto com chave 'products'")
            return None
            
    except json.JSONDecodeError as e:
        print(f"✗ Erro ao ler JSON: {e}")
        return None
    except Exception as e:
        print(f"✗ Erro ao carregar arquivo: {e}")
        return None

def get_demo_products() -> List[Dict]:
    """
    Return demo product data for testing
    
    Returns:
        List of demo product dictionaries
    """
    return [
        {
            "name": "Óculos de Sol Aviador Classic",
            "price": 89.90,
            "url": "https://www.zerezes.com.br/produto/aviador-classic"
        },
        {
            "name": "Óculos de Grau Retangular Metal",
            "price": 129.90,
            "url": "https://www.zerezes.com.br/produto/retangular-metal"
        },
        {
            "name": "Óculos de Sol Wayfarer Style",
            "price": 79.90,
            "url": "https://www.zerezes.com.br/produto/wayfarer-style"
        },
        {
            "name": "Óculos de Grau Redondo Acetato",
            "price": 149.90,
            "url": "https://www.zerezes.com.br/produto/redondo-acetato"
        },
        {
            "name": "Óculos de Sol Esportivo Polarizado",
            "price": 159.90,
            "url": "https://www.zerezes.com.br/produto/esportivo-polarizado"
        },
        {
            "name": "Óculos de Grau Gatinho Fashion",
            "price": 99.90,
            "url": "https://www.zerezes.com.br/produto/gatinho-fashion"
        },
        {
            "name": "Óculos de Sol Hexagonal Moderno",
            "price": 69.90,
            "url": "https://www.zerezes.com.br/produto/hexagonal-moderno"
        },
        {
            "name": "Óculos de Leitura +2.00",
            "price": 39.90,
            "url": "https://www.zerezes.com.br/produto/leitura-200"
        }
    ]

def find_cheapest_glasses(products: List[Dict]) -> Optional[Dict]:
    """
    Find the cheapest glasses from the product list
    
    Args:
        products: List of product dictionaries with 'name' and 'price' keys
        
    Returns:
        Dictionary with cheapest product info or None if list is empty
    """
    if not products:
        return None
    
    # Filter for glasses/eyewear products if needed
    glasses = [p for p in products if 'oculos' in p.get('name', '').lower() 
               or 'glass' in p.get('name', '').lower()
               or 'óculos' in p.get('name', '').lower()]
    
    if not glasses:
        glasses = products  # Use all products if no specific glasses found
    
    # Find the cheapest one
    cheapest = min(glasses, key=lambda x: x.get('price', float('inf')))
    return cheapest

def display_results(products: List[Dict], cheapest: Dict):
    """
    Display the results in a formatted way
    
    Args:
        products: List of all products
        cheapest: The cheapest product found
    """
    print("\n" + "=" * 70)
    print("RESULTADO DA BUSCA")
    print("=" * 70)
    
    print(f"\n📊 Total de produtos encontrados: {len(products)}")
    
    if products:
        print("\n🏷️  TODOS OS PRODUTOS:")
        print("-" * 70)
        # Sort by price to show all products in order
        sorted_products = sorted(products, key=lambda x: x.get('price', 0))
        for i, product in enumerate(sorted_products, 1):
            marker = "👉 " if product == cheapest else "   "
            print(f"{marker}{i}. {product.get('name', 'N/A'):<45} R$ {product.get('price', 0):>7.2f}")
    
    print("\n" + "=" * 70)
    if cheapest:
        print("🏆 ÓCULOS MAIS BARATO:")
        print("=" * 70)
        print(f"  📝 Nome: {cheapest.get('name', 'N/A')}")
        print(f"  💰 Preço: R$ {cheapest.get('price', 0):.2f}")
        if cheapest.get('url'):
            print(f"  🔗 Link: {cheapest.get('url', 'N/A')}")
    else:
        print("✗ Nenhum produto encontrado")
    
    print("=" * 70)
    print()

def main():
    """
    Main function to execute the script
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Encontrar os óculos mais baratos da Zerezes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos de uso:
  python3 find_cheapest_glasses.py                      # Tentar web scraping
  python3 find_cheapest_glasses.py --demo              # Usar dados de demonstração
  python3 find_cheapest_glasses.py --data products.json # Carregar de arquivo JSON

Formato do arquivo JSON:
  [
    {"name": "Nome do Produto", "price": 99.90, "url": "https://..."},
    ...
  ]
        '''
    )
    parser.add_argument('--data', type=str, help='Caminho para arquivo JSON com dados dos produtos')
    parser.add_argument('--demo', action='store_true', help='Usar dados de demonstração')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("BUSCADOR DE ÓCULOS MAIS BARATOS DA ZEREZES")
    print("=" * 70)
    print()
    
    products = None
    
    # Determine which mode to use
    if args.demo:
        print("🎭 Modo de demonstração ativado")
        print()
        products = get_demo_products()
    elif args.data:
        print(f"📂 Carregando dados do arquivo: {args.data}")
        print()
        products = load_products_from_json(args.data)
    else:
        print("🌐 Tentando acessar o site da Zerezes...")
        print()
        products = fetch_zerezes_products()
    
    # Check if we got products
    if products is None or len(products) == 0:
        print("\n⚠ Não foi possível obter dados dos produtos.")
        
        if not args.demo and not args.data:
            print("⚠ Isso pode ser devido a:")
            print("  - Restrições de rede no ambiente de execução")
            print("  - O site pode estar fora do ar")
            print("  - O site pode bloquear acessos automatizados")
            print()
            print("💡 Soluções alternativas:")
            print("  1. Execute com dados de demonstração:")
            print("     python3 find_cheapest_glasses.py --demo")
            print()
            print("  2. Forneça um arquivo JSON com os dados:")
            print("     python3 find_cheapest_glasses.py --data products.json")
            print()
            print("  3. Execute em um ambiente com acesso completo à internet")
        
        sys.exit(1)
    
    # Find the cheapest glasses
    cheapest = find_cheapest_glasses(products)
    
    # Display results
    display_results(products, cheapest)

if __name__ == "__main__":
    main()
