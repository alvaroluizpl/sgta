# Path facilita montar caminhos de pastas de forma compatível com qualquer SO.
from pathlib import Path

# config() lê variáveis do arquivo .env em vez de deixar senhas fixas no código.
from decouple import config


# Caminho base do projeto
# __file__ é o caminho deste arquivo (settings.py).
# .parent.parent sobe duas pastas: config/ → backend/ — que é a raiz do projeto.
# BASE_DIR é usado abaixo para montar outros caminhos relativos ao projeto.
BASE_DIR = Path(__file__).resolve().parent.parent


# Segurança
# Chave secreta usada pelo Django para assinar cookies, tokens e sessões.
# Lida do .env para não ficar exposta no código — nunca commite a chave real.
SECRET_KEY = config('SECRET_KEY', default='django-insecure-sgta-dev-key-troque-em-producao')

# Modo de depuração: True mostra erros detalhados no navegador.
# Em produção DEVE ser False — nunca suba com DEBUG=True em servidor real.
# cast=bool converte a string "True"/"False" do .env para booleano Python.
DEBUG = config('DEBUG', default=True, cast=bool)

# Lista de domínios que podem acessar a aplicação.
# '*' aceita qualquer domínio — adequado para desenvolvimento local.
# Em produção, liste apenas os domínios reais: ['meusite.com', 'www.meusite.com']
ALLOWED_HOSTS = ['*']


# Apps instalados 
# Lista de todos os apps que o Django deve carregar.
# Os seis primeiros são apps internos do Django (admin, autenticação, etc.).
# Os dois últimos são os apps que criamos neste projeto.
INSTALLED_APPS = [
    'django.contrib.admin',        # painel de administração em /admin
    'django.contrib.auth',         # sistema de autenticação e permissões
    'django.contrib.contenttypes', # framework para tipos de conteúdo genéricos
    'django.contrib.sessions',     # gerenciamento de sessões de usuário
    'django.contrib.messages',     # sistema de mensagens flash (ex.: "salvo com sucesso")
    'django.contrib.staticfiles',  # serve arquivos estáticos (CSS, JS, imagens)
    'tarefas',                     # nosso app de tarefas acadêmicas
    'usuarios',                    # nosso app de usuários
]


# Middlewares 
# Middlewares são camadas que toda requisição HTTP atravessa antes de chegar na view
# e toda resposta atravessa antes de voltar ao navegador — como uma fila de filtros.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # headers de segurança (HTTPS, etc.)
    'django.contrib.sessions.middleware.SessionMiddleware',     # gerencia a sessão do usuário
    'django.middleware.common.CommonMiddleware',                # normaliza URLs (ex.: adiciona barra final)
    'django.middleware.csrf.CsrfViewMiddleware',                # proteção contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # associa o usuário logado à requisição
    'django.contrib.messages.middleware.MessageMiddleware',     # habilita as mensagens flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # proteção contra clickjacking
]


# URLs 
# Indica qual arquivo é o ponto de entrada das URLs do projeto.
# O Django vai olhar config/urls.py para rotear as requisições.
ROOT_URLCONF = 'config.urls'


# Templates
# Configuração do sistema de templates (HTML dinâmico).
# Usamos o motor padrão do Django. APP_DIRS=True faz o Django procurar
# templates dentro da pasta templates/ de cada app automaticamente.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI 
# WSGI é o protocolo que conecta o Django ao servidor web (ex.: Gunicorn, uWSGI).
# Aponta para o arquivo wsgi.py que inicializa a aplicação.
WSGI_APPLICATION = 'config.wsgi.application'


# Banco de dados
# Antes usávamos SQLite (um arquivo local). Agora usamos PostgreSQL rodando
# em um container Docker separado, chamado "db" no docker-compose.yml.
# Todos os valores são lidos do .env — nenhuma senha fica exposta no código.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # diz ao Django para usar PostgreSQL
        'NAME': config('DB_NAME'),                  # nome do banco de dados
        'USER': config('DB_USER'),                  # usuário do banco
        'PASSWORD': config('DB_PASSWORD'),          # senha do usuário
        'HOST': config('DB_HOST', default='db'),    # "db" é o nome do service no docker-compose
        'PORT': config('DB_PORT', default='5432'),  # porta padrão do PostgreSQL
    }
}


# Validação de senhas 
# Regras aplicadas quando um usuário cria ou altera a senha no sistema.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # senha não pode ser parecida com o nome
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},             # mínimo de 8 caracteres
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},            # bloqueia senhas óbvias como "123456"
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},           # senha não pode ser só números
]


# Internacionalização 
LANGUAGE_CODE = 'pt-br'            # idioma padrão da interface do admin
TIME_ZONE = 'America/Sao_Paulo'    # fuso horário usado em datas e horas
USE_I18N = True                    # habilita o sistema de tradução do Django
USE_TZ = True                      # armazena datas em UTC no banco e converte para TIME_ZONE na exibição


# Arquivos estáticos 
# URL base para servir arquivos estáticos (CSS, JS, imagens).
# Ex.: /static/admin/css/base.css
STATIC_URL = 'static/'


# Chave primária padrão
# Define o tipo do campo "id" gerado automaticamente em todos os models.
# BigAutoField usa inteiro de 64 bits — suporta até 9 quintilhões de registros.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
