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
sudo apt install git -y
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


## Criando um repositório no servidor

Um repositório bare é um repositório transitório (como se fosse um github).

```
mkdir -p ~/app_bare
cd ~/app_bare
git init --bare
cd ~
```

Criando o repositório da aplicação

```
mkdir -p ~/app_repo
cd ~/app_repo
git init
git remote add origin ~/app_bare
git add . && git commit -m 'Initial'
cd ~
```

No seu computador local, adicione o bare como remoto:

```
git remote add app_bare masterchef:~/app_bare
git push app_bare <branch>
```

No servidor, em app_repo, faça pull:

```
cd ~/app_repo
git pull origin <branch>
```


## Criando o ambiente virtual

```
cd  ~/app_repo
git pull origin <branch>
python3.9 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install psycopg2
pip install gunicorn
```

## Configurando o nginx

###############################################################################
# Replace
# ___GUNICORN_FILE_NAME___ to the name of the gunicorn file you want
# __YOUR_USER__ to your user name
# __PROJECT_FOLDER__ to the folder name of your project
# __WSGI_FOLDER__ to the folder name where you find a file called wsgi.py
#
###############################################################################
# Criando o arquivo ___GUNICORN_FILE_NAME___.socket
sudo nano /etc/systemd/system/___GUNICORN_FILE_NAME___.socket

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=gunicorn blog socket

[Socket]
ListenStream=/run/___GUNICORN_FILE_NAME___.socket

[Install]
WantedBy=sockets.target

###############################################################################
# Criando o arquivo ___GUNICORN_FILE_NAME___.service
sudo nano /etc/systemd/system/___GUNICORN_FILE_NAME___.service

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=Gunicorn daemon (You can change if you want)
Requires=___GUNICORN_FILE_NAME___.socket
After=network.target

[Service]
User=__YOUR_USER__
Group=www-data
Restart=on-failure
EnvironmentFile=/home/__YOUR_USER__/__PROJECT_FOLDER__/.env
WorkingDirectory=/home/__YOUR_USER__/__PROJECT_FOLDER__
# --error-logfile --enable-stdio-inheritance --log-level and --capture-output
# are all for debugging purposes.
ExecStart=/home/__YOUR_USER__/__PROJECT_FOLDER__/venv/bin/gunicorn \
          --error-logfile /home/__YOUR_USER__/__PROJECT_FOLDER__/gunicorn-error-log \
          --enable-stdio-inheritance \
          --log-level "debug" \
          --capture-output \
          --access-logfile - \
          --workers 6 \
          --bind unix:/run/___GUNICORN_FILE_NAME___.socket \
          __WSGI_FOLDER__.wsgi:application

[Install]
WantedBy=multi-user.target

###############################################################################
# Ativando
sudo systemctl start ___GUNICORN_FILE_NAME___.socket
sudo systemctl enable ___GUNICORN_FILE_NAME___.socket

# Checando
sudo systemctl status ___GUNICORN_FILE_NAME___.socket
curl --unix-socket /run/___GUNICORN_FILE_NAME___.socket localhost
sudo systemctl status ___GUNICORN_FILE_NAME___

# Restarting
sudo systemctl restart ___GUNICORN_FILE_NAME___.service
sudo systemctl restart ___GUNICORN_FILE_NAME___.socket
sudo systemctl restart ___GUNICORN_FILE_NAME___

# After changing something
sudo systemctl daemon-reload

# Debugging
sudo journalctl -u ___GUNICORN_FILE_NAME___.service
sudo journalctl -u ___GUNICORN_FILE_NAME___.socket
