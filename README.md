# DeliveryDjangoPos
Trabalho de projeto das disciplina Framework na Pós de Agentes Inteligentes do INF/UFG.
Essa aplicação envolve gestão de pedidos de um delivery controlado por meio de uma interface conversacional. 


- Para iniciar a configuraçoes inicais
```
python -m pip install --upgrade pip
python -m venv .venv
source .venv/bin/activate
```

- Para instalar a biblioteca Django
``` pip install django ```

- Para instalar a biblioteca Bootstrap
``` pip install django-bootstrap-v5 ```

- Para instalar a biblioteca Pandas
``` pip install pandas ```

- Para instalar a biblioteca FastAPI
``` pip install "fastapi[standard]" ```

- Para instalar a biblioteca para usar o Dotenv pra carregar configuracoes e chaves api 
``` pip install python-dotent ```

- Para instalar o GROQ, orquestrador de LLM
``` pip install groq ```

- Entrar na pasta *delivery/*
``` cd delivery/ ``` 

- Pra rodar o projeto Django
``` cd delivery/
    python manage.py makemigrations gestor
    python manage.py migrate
    python manage.py runserver 
    python manage.py startapp delivery
    python manage.py startapp chatbot
```


- Pra rodar o projeto Fastapi
``` fastapi dev main.py ```

- Pra rodar o Webhoook
``` python webhook.py ```

