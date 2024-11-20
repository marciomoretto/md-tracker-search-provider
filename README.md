# MD Tracker Search Provider
O MD Tracker Search Provider é uma extensão para o Gnome Shell que permite realizar buscas rápidas e organizadas de arquivos Markdown monitorados pelo MD Tracker. Ele facilita a navegação e a relação entre arquivos .md, identificando conexões e dependências entre eles.

## Funcionalidades
* **Integração com o Gnome Shell:** Busca diretamente nos arquivos monitorados pelo MD Tracker através da interface do Gnome Shell.
* **Busca por arquivos relacionados:** Permite localizar arquivos .md conectados ao arquivo atual ou os arquivos que ele referencia.
* **Monitoramento contínuo:** Aproveita as atualizações do MD Tracker para manter os dados sempre sincronizados.

## Pré-requisitos
* **MD Tracker** instalado e configurado corretamente.
* **Sistema Operacional:** Linux com Gnome Shell.
* **Dependências adicionais** (o gerenciador de pacotes pode solicitá-las automaticamente durante a instalação).

## Instalação
* Baixar o pacote .deb:
  Faça o download do arquivo `.deb` mais recente a partir do repositório ou da página oficial do projeto.

* Instalar o pacote:

  Use o dpkg para instalar o pacote:

  ```bash
  sudo dpkg -i md-tracker-search-provider.deb
  ```

* Resolver dependências:

  Caso apareçam mensagens de dependências ausentes, instale-as com:

  ```bash
  sudo apt-get install -f
  ```
  
* Verificar a configuração:

  Certifique-se de que o arquivo de configuração do MD Tracker Search Provider está correto. O arquivo de configuração deve estar localizado em:
  ```
  ~/.config/md-tracker/config
  ```
  Ele deve conter o seguinte:
  ```bash
  $PAGES_DIR=<CAMINHOPARAAPASTA>
  ```

## Uso
Depois de instalado e configurado:

1. Pressione `Super` (tecla Windows ou equivalente) para abrir a pesquisa do Gnome Shell.
2. Digite um termo relacionado a um arquivo `.md` ou a referência que você deseja buscar.
3. O MD Tracker Search Provider exibirá os resultados relacionados no menu de busca.

## Contribuindo
Contribuições são bem-vindas! Veja como você pode ajudar:

1. Faça um fork do repositório.
2. Crie um branch para sua funcionalidade ou correção: `git checkout -b minha-contribuicao.`
3. Envie suas alterações em um Pull Request.

## Licença
Este projeto está licenciado sob a Licença GPL 3.0. Consulte o arquivo LICENSE para mais detalhes.
