# Simple Search Provider

O Simple Search Provider é um provedor de busca para o GNOME Shell que utiliza o Tracker3 para oferecer uma busca eficiente e personalizada de arquivos. Ele suporta busca de arquivos relacionados até dois graus de separação, integrando-se perfeitamente ao ambiente do GNOME.

## Recursos
**Busca Avançada:** Explora relações semânticas entre arquivos no sistema de metadados RDF do Tracker3, permitindo localizar não apenas arquivos diretamente relacionados ao termo pesquisado, mas também aqueles conectados indiretamente por até dois níveis de separação.
**Integração com GNOME:** Suporte ao protocolo D-Bus para se comunicar diretamente com o GNOME Shell.
**Rápido e Eficiente:** Usa Tracker3 para consultas rápidas com suporte a RDF.

## Requisitos
* **Sistema Operacional:** Linux com GNOME Shell.
* **Dependências:** As dependências são instaladas automaticamente ao usar o .deb, mas para instalações manuais, você precisa:
  * Python 3
  * Python bindings for GTK (python3-gi)
  * Tracker3
  * D-Bus

## Instalação

### Opção 1: Usando o .deb
1. Baixe o arquivo .deb disponível na página de releases.

2. Instale o pacote:

```bash
sudo dpkg -i simple-search-provider.deb
```

3. Verifique se o serviço está funcionando:

```bash
systemctl --user status simple-search-provider.service
```

4. Caso haja problemas com dependências, resolva-as com:

```bash
sudo apt --fix-broken install
```

### Opção 2: Usando o Makefile
1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/simple-search-provider.git
cd simple-search-provider
```

2. Instale e configure o provedor:

```bash
make all
```

3. Verifique o status do serviço:

```bash
systemctl --user status simple-search-provider.service
```

## Uso
1. Abra o menu de busca do GNOME Shell (pressione Super ou Windows).
2. Digite um termo relacionado ao arquivo que deseja buscar.
3. Veja os resultados diretamente no GNOME Shell.

## Desinstalação
### Com o `.deb`
Remova o pacote:
```bash
sudo apt remove simple-search-provider
```

### Com o Makefile
Execute:
```bash
make uninstall
```

## Desenvolvimento
Se quiser contribuir, siga os passos abaixo:

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/simple-search-provider.git
cd simple-search-provider
```

Teste localmente:

```bash
python3 simple_search_provider.py
```

Envie um Pull Request com suas melhorias ou correções.

## Licença
Este projeto é licenciado sob a GPL-3.0. Veja o arquivo LICENSE para mais informações.

Contribuidores
Seu Nome - Desenvolvedor principal.
Se você gostou deste projeto ou encontrou um problema, sinta-se à vontade para abrir uma issue.

