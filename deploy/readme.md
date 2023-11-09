1. Setar nas configurações do .env o banco de dados que deseja usar
2. Configurar  ALLOWED_HOSTS e DEBUG para poder fazer Deploy
3. Criar o SSH para conexão com servidor
4. Atualizar todos os pacotes abaixo
    sudo apt update -y
    sudo apt upgrade -y
    sudo apt autoremove -y
    sudo apt install build-essential -y
    sudo apt install python3.9 python3.9-venv python3.9-dev -y
    sudo apt install nginx -y
    sudo apt install certbot python3-certbot-nginx -y
    sudo apt install postgresql postgresql-contrib -y
    sudo apt install libpq-dev -y
    sudo apt install git