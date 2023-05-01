
# Fitter Happier API

Uma API para criação e acompanhamento de treinos e exercício físico no geral a partir de vídeos do youtube.




## Instalação

1. Clone o projeto e certifique-se de estar na branch `main`
2. Instalação sem Docker
2.1 Crie um ambiente virtual do Python (virtualenv) para instalação das dependências.

2.2 Com o ambiente virtual ativo, rode o comando na raiz do projeto: 
```bash
  pip install requirements.txt
```
2.3 Após a instalação terminar, rode o projeto com o comando:
```bash
  flask run --reload
```

3. Instalação com Docker
  3.1 Na raiz do projeto, crie a imagem:
```bash
  docker build -t rest-apis-flask-python .
```
  3.2 Rode a imagem criada:
```bash
  docker run -p 5000:5000 rest-apis-flask-python
```
    
## Documentação

Após rodar o projeto, é possível acessar a documentação da API no swagger acessando a `url local + /doc`. Exemplo para porta 5000: http://localhost:5000/doc
