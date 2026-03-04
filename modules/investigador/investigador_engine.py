import requests
import json
import urllib.parse
from bs4 import BeautifulSoup
import sys
import os

class InvestigatorEngine:
    def __init__(self, config_path=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def investigar(self, query, num_results=5):
        """Busca en Google con selectores actualizados."""
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=es"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            results = []
            
            # Selector genérico para resultados de búsqueda modernos
            for g in soup.select('div.tF2Cxc'):
                if len(results) >= num_results: break
                title = g.select_one('h3')
                link = g.select_one('a')
                snippet = g.select_one('div.VwiC3b')
                
                if title and link:
                    results.append({
                        "titulo": title.get_text(),
                        "link": link['href'],
                        "resumen": snippet.get_text() if snippet else "N/A"
                    })
            return results
        except Exception as e:
            return [{"error": str(e)}]

    def oteador(self, urls):
        hallazgos = []
        for url in urls:
            try:
                res = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(res.text, "html.parser")
                # Extraer texto de párrafos principalmente
                text = "\n".join([p.get_text() for p in soup.find_all('p')])
                hallazgos.append({"url": url, "content": text[:2000]})
            except Exception as e:
                hallazgos.append({"url": url, "error": str(e)})
        return hallazgos

    def consultar_docs(self, tema=None):
        return "Docs system ready."
