1. Setar nas configurações do .env o banco de dados que deseja usar
2. Configurar  ALLOWED_HOSTS e DEBUG para poder fazer Deploy
3. Criar o SSH para conexão com servidor
4. Atualizar todos os pacotes abaixo
```
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install python3.10 python3.10-venv python3.10-dev -y
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git
```


5. Configurar o Postgres

### Configurações
```
sudo -u postgres psql

# Criando um super usuário
CREATE ROLE masterchef WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'm45t3rch3f!';

# Criando a base de dados
CREATE DATABASE masterchef WITH OWNER masterchef;

# Dando permissões
GRANT ALL PRIVILEGES ON DATABASE masterchef TO masterchef;
# Saindo
\q
sudo systemctl restart postgresql
```

6. Configurar o Git

```
git config --global user.name 'Seu nome'
git config --global user.email 'seu_email@gmail.com'
git config --global init.defaultBranch main
```