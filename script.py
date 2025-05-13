import requests
import json

# =================== CONFIGURAÇÕES ===================
API_TOKEN = "sv6ravJXyeoxviYzYCiKf3sMlG9ZBfT2s7qsGavgahY"  # Substitua pelo seu token WPScan
SITE = "http://exemplo.com.br"  # Substitua pela URL do WordPress
COMMON_PLUGINS = [
    "contact-form-7", "elementor", "woocommerce", "yoast-seo",
    "wordfence", "akismet", "jetpack", "updraftplus"
]
# =====================================================

def plugin_existe(plugin_name):
    url = f"{SITE}/wp-content/plugins/{plugin_name}/"
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False

def obter_versao_plugin(plugin_name):
    url = f"{SITE}/wp-content/plugins/{plugin_name}/readme.txt"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and "Stable tag:" in r.text:
            for line in r.text.splitlines():
                if "Stable tag:" in line:
                    return line.split("Stable tag:")[1].strip()
    except:
        pass
    return None

def consultar_wpscan(plugin_name):
    headers = {"Authorization": f"Token token={API_TOKEN}"}
    response = requests.get(
        f"https://wpscan.com/api/v3/plugins/{plugin_name}",
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    return None

def verificar_vulnerabilidades(plugin_name, versao_encontrada):
    dados = consultar_wpscan(plugin_name)
    if not dados or "vulnerabilities" not in dados:
        return

    print(f"\n🔍 Plugin: {plugin_name}")
    print(f"   ↪ Versão encontrada: {versao_encontrada or 'Não detectada'}")

    encontrou = False
    for v in dados["vulnerabilities"]:
        title = v.get("title", "Sem título")
        fixed_in = v.get("fixed_in", "Desconhecido")
        affected_versions = v.get("vulnerable_versions", "N/A")
        url = v.get("references", {}).get("url", [""])[0]

        print("   ⚠️ Vulnerabilidade encontrada:")
        print(f"      - Título: {title}")
        print(f"      - Afeta versões: {affected_versions}")
        print(f"      - Corrigido em: {fixed_in}")
        print(f"      - Mais info: {url}")
        encontrou = True

    if not encontrou:
        print("   ✅ Nenhuma vulnerabilidade conhecida encontrada.")

# ============== EXECUÇÃO PRINCIPAL ===================

print("🚀 Iniciando varredura de plugins no WordPress...")

for plugin in COMMON_PLUGINS:
    if plugin_existe(plugin):
        versao = obter_versao_plugin(plugin)
        verificar_vulnerabilidades(plugin, versao)

print("\n✅ Varredura concluída.")

