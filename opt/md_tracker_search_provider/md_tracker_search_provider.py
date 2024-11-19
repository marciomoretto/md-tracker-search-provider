#!venv/bin/python3

import os
import dbus
import dbus.service
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import subprocess
import urllib.parse
import re
import mimetypes
import logging

# Caminho do arquivo de log
LOG_FILE = os.path.expanduser("/var/log/md-tracker-search_provider.log")

# Configuração básica de logging
logging.basicConfig(
    level=logging.DEBUG,  # Registrar mensagens de DEBUG e acima
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Salvar logs no arquivo
        logging.StreamHandler()  # Mostrar logs no terminal
    ]
)

logging.info("MD Tracker Search Provider iniciado. Logs salvos em: %s", LOG_FILE)

DBusGMainLoop(set_as_default=True)

# Caminho do arquivo de configuração
CONFIG_FILE = os.path.expanduser("~/.config/md_tracker/config")

def load_base_dir(config_file):
    """
    Carrega o BASE_DIR do arquivo de configuração.
    """
    try:
        with open(config_file, "r") as f:
            for line in f:
                # Busca pela linha que define BASE_DIR
                if line.startswith("BASE_DIR="):
                    return line.split("=", 1)[1].strip()  # Remove espaços e quebras de linha
    except FileNotFoundError:
        logging.error("Arquivo de configuração não encontrado: %s", config_file)
    except Exception as e:
        logging.error("Erro ao ler o arquivo de configuração: %s", e)

    # Caminho padrão se não for encontrado no arquivo
    return os.path.expanduser("~/Documentos/Vault/pages/")

# Carregar o BASE_DIR
BASE_DIR = load_base_dir(CONFIG_FILE)
logging.info("BASE_DIR configurado como: %s", BASE_DIR)

class MDTrackerSearchProvider(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName("org.example.MDTrackerSearch", bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, "/org/example/MDTrackerSearch/SearchProvider2")

    @dbus.service.method("org.gnome.Shell.SearchProvider2", in_signature="as", out_signature="as")
    def GetInitialResultSet(self, terms):
        """
        Captura os termos digitados na barra de busca e retorna os resultados iniciais.
        """
        if not terms:
            return []

        return []

    @dbus.service.method("org.gnome.Shell.SearchProvider2", in_signature="asas", out_signature="as")
    def GetSubsearchResultSet(self, previous_results, new_terms):
        """
        Refina os resultados com base em pesquisas adicionais.
        """

        keyword = ' '.join(str(item) for item in new_terms)

        # Ignorar entradas curtas
        if len(keyword) < 4:
             return []  # Retorna vazio se o termo for menor que 4 caracteres

        # Buscar arquivos relacionados ao arquivo alvo
        return self.search_files_two_hops(keyword)

    @dbus.service.method("org.gnome.Shell.SearchProvider2", in_signature="as", out_signature="aa{sv}")
    def GetResultMetas(self, identifiers):
        """
        Retorna metadados sobre os resultados, incluindo ícone e descrição baseados no tipo MIME.
        Se nenhuma descrição específica estiver disponível, utiliza o caminho do arquivo como descrição.
        """
        metas = []

        for identifier in identifiers:
            # Extrair ?file e ?file1 do par
            file, file1 = identifier.split("|", 1)

            # Determinar o nome do arquivo
            name = os.path.basename(file1)

            # Extrair apenas o nome base do arquivo original (sem extensão)
            description = os.path.splitext(os.path.basename(file))[0]

            # Determinar o tipo MIME
            mime_type, _ = mimetypes.guess_type(file1)

            # Atribuir um ícone baseado no tipo MIME
            if mime_type and mime_type.startswith("text/"):
                icon = "text-x-generic"
            elif mime_type and mime_type.startswith("image/"):
                icon = "image-x-generic"
            elif mime_type and mime_type.startswith("audio/"):
                icon = "audio-x-generic"
            elif mime_type and mime_type.startswith("video/"):
                icon = "video-x-generic"
            else:
                icon = "application-x-generic"

            # Adicionar metadados à lista
            metas.append({
                "id": file1,  # Identificador único    
                "name": name,  # Nome do arquivo
                "description": description,  # Descrição do arquivo (ou caminho como fallback)
                "icon": icon,  # Ícone representando o tipo
            })

        return metas

    @dbus.service.method("org.gnome.Shell.SearchProvider2", in_signature="s", out_signature="")
    def ActivateResult(self, identifier):
        """
        Abre o arquivo no Nautilus ou em outro programa associado.
        """
        subprocess.run(["xdg-open", identifier])

    def search_files_two_hops(self, keyword):
        """
        Realiza a busca dos arquivos relacionados.
        """
        def execute_sparql_query(query):
            """
            Executa a consulta SPARQL e retorna pares organizados de URIs.
            """
            try:
                result = subprocess.run(
                    ["tracker3", "sparql", "--dbus-service=org.freedesktop.Tracker3.Miner.Files", "-q", query],
                    stdout=subprocess.PIPE, text=True, check=True
                )
                matches = re.findall(r'file://[^\s]+', result.stdout)

                # Organizar pares
                files = []
                for i in range(0, len(matches), 2):
                    if i + 1 < len(matches):  # Verifica se há um par completo
                        file = matches[i]
                        related_file = matches[i + 1]
                        files.append((file, related_file))
                return files
            except subprocess.CalledProcessError as e:
                logging.error("Erro ao executar a consulta SPARQL: %s", e)
                return []

        def format_results(pairs):
            """
            Formata os resultados como 'file|related_file', aplicando filtros.
            """
            return [
                f"{urllib.parse.unquote(file.replace('file://', '').strip())}|{urllib.parse.unquote(related_file.replace('file://', '').strip())}"
                for file, related_file in pairs
                if not related_file.endswith(".md")
            ]
        
        parsed_kw = urllib.parse.quote(keyword, safe='')

        query_first_hop = f"""
        SELECT ?file ?file1 WHERE {{
            ?file nie:relatedTo ?file1 .
            FILTER(CONTAINS(LCASE(STR(?file)), LCASE(\"{parsed_kw}\")))
        }}
        """
        query_second_hop = f"""
        SELECT ?file ?file2 WHERE {{
            ?file nie:relatedTo ?intermediate .
            ?intermediate nie:relatedTo ?file2 .
            FILTER(CONTAINS(LCASE(STR(?file)), LCASE(\"{parsed_kw}\")))
        }}
        """
    
        files_first_hop = execute_sparql_query(query_first_hop)
        files_second_hop = execute_sparql_query(query_second_hop)
        combined_results = format_results(files_first_hop) + format_results(files_second_hop)
        return combined_results

          
if __name__ == "__main__":
    loop = GLib.MainLoop()
    provider = MDTrackerSearchProvider()
    print("MD Tracker Search Provider iniciado.")
    loop.run()
