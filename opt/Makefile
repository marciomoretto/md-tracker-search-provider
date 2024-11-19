# ======================= INSTRUÇÕES ==========================
# Este Makefile é utilizado para construir, instalar e desinstalar
# o pacote do Simple Search Provider. Ele segue a estrutura de diretórios
# recomendada para pacotes .deb.
#
# COMANDOS DISPONÍVEIS:
#
# 1. Construir o pacote .deb:
#    make build
#
# 2. Instalar o pacote:
#    make install
#
# 3. Desinstalar o pacote:
#    make uninstall
#
# 4. Limpar arquivos temporários:
#    make clean

# Variáveis de Configuração
PACKAGE_NAME = simple-search-provider
BUILD_DIR = $(PACKAGE_NAME)
DEB_PACKAGE = $(PACKAGE_NAME).deb

BIN_DIR = $(BUILD_DIR)/usr/local/bin
DBUS_DIR = $(BUILD_DIR)/etc/dbus-1/services
SYSTEMD_USER_DIR = $(BUILD_DIR)/lib/systemd/user

# Alvos principais
.PHONY: all build install clean uninstall

# Alvo principal
all: build

# Construir o pacote .deb
build:
	@echo "Criando estrutura do pacote..."
	# Criar diretórios necessários
	mkdir -p $(BIN_DIR)
	mkdir -p $(DBUS_DIR)
	mkdir -p $(SYSTEMD_USER_DIR)
	mkdir -p $(BUILD_DIR)/DEBIAN

	# Copiar arquivos do projeto para os diretórios correspondentes
	install -m 0755 simple_search_provider.py $(BIN_DIR)/
	install -m 0644 org.example.SimpleSearch.service $(DBUS_DIR)/
	install -m 0644 simple-search-provider.service $(SYSTEMD_USER_DIR)/

	# Configurar os scripts de controle do pacote
	install -m 0755 DEBIAN/postinst $(BUILD_DIR)/DEBIAN/postinst
	install -m 0755 DEBIAN/prerm $(BUILD_DIR)/DEBIAN/prerm
	install -m 0644 DEBIAN/control $(BUILD_DIR)/DEBIAN/control

	# Criar o pacote .deb
	@echo "Empacotando $(DEB_PACKAGE)..."
	dpkg-deb --build $(BUILD_DIR)
	@echo "Pacote $(DEB_PACKAGE) criado com sucesso!"

# Instalar o pacote .deb
install: build
	@echo "Instalando $(DEB_PACKAGE)..."
	sudo dpkg -i $(DEB_PACKAGE)
	@echo "Pacote instalado com sucesso!"

# Desinstalar o pacote
uninstall:
	@echo "Removendo o pacote $(PACKAGE_NAME)..."
	sudo apt remove -y $(PACKAGE_NAME)
	@echo "Pacote removido com sucesso!"

# Limpar arquivos de construção
clean:
	@echo "Limpando arquivos temporários..."
	rm -rf $(BUILD_DIR) $(DEB_PACKAGE)
	@echo "Limpeza concluída!"
