# GenFit

GenFit é uma aplicação web que gera automaticamente rotinas de exercícios físicos personalizadas com base nas necessidades do usuário. Promovemos saúde e direcionamento específico, disponibilizando todos os serviços gratuitamente.

---

## 🛠️ Instruções de Instalação e Uso

Siga os passos abaixo para configurar e executar o GenFit localmente:

### 1. Faça um Fork do Repositório no GitHub

1. Acesse o repositório oficial do GenFit no GitHub.
2. Clique no botão **Fork** no canto superior direito da página.
3. O repositório será copiado para sua conta do GitHub.

### 2. Clone o Repositório

Após fazer o fork, clone o repositório para a sua máquina:

``` bash
git clone https://github.com/<SEU_USUARIO>/genfit-app
```

### 3. Navegue até o diretorio do projeto

```bash
cd GenFit
```
### 4. Crie um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente:

  ```bash
  venv/Scripts/activate
  ```
### 5. Instale as dependências
 Todas as dependências necessárias serão instaladas seguindo este comando
```bash
pip install -r requirements.txt
```

### 6. Instale o Ollama
Link para baixar o Ollama: https://ollama.com/


#### 6.1. Rode o Llama 3.2

```bash
  ollama run llama3.2
```
Isso irá instalar o Llama 3.2 fazendo-o ficar disponível localmente e possibilitando o funcionamento da aplicação (GenFit).


### 7. Execução da aplicação

```bash
python app.py 

ou

python3 app.py
```

Acesse a aplicação em: http://127.0.0.1:5000.


  


