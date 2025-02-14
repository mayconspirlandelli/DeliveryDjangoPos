# DeliveryDjangoPos
Trabalho de projeto das disciplina Framework na Pós de Agentes Inteligentes do INF/UFG.
Essa aplicação envolve gestão de pedidos de um delivery controlado por meio de uma interface conversacional. 


- Para iniciar a configuraçoes inicais
```
python -m pip install —upgrade pip
python -m venv .venv
source .venv/bin/activate
```

- Para instalar a biblioteca Django
``` pip install django ```

- Para instalar a biblioteca FastAPI
``` pip install "fastapi[standard]" ```

- Para instalar a biblioteca para usar o Dotenv pra carregar configuracoes e chaves api 
``` pip install python-dotent ```

- Para instalar o GROQ, orquestrador de LLM
``` pip install groq ```

- Pra rodar o projeto Fastapi
``` fastapi dev main.py ```

- Pra rodar o projeto Django
``` fastapi dev main.py ```

- Pra rodar o Webhoook
``` python webhook.py ```

