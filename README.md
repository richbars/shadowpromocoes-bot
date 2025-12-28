# 🤖 Shadow Promoções Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-green?style=for-the-badge)

O **Shadow Promoções Bot** é uma automação desenvolvida em Python projetada para monitorar ofertas no **Mercado Livre** e enviá-las automaticamente para um canal do **Telegram**. O sistema utiliza uma arquitetura limpa e modular para garantir escalabilidade e fácil manutenção.

---

## 🚀 Funcionalidades

- **🔍 Monitoramento Contínuo**: Verifica periodicamente novas promoções no Mercado Livre.
- **📢 Integração com Telegram**: Envia alertas formatados com imagem, preço, desconto e link de afiliado.
- **💾 Persistência de Dados**: Utiliza SQLite para armazenar histórico e evitar o envio de ofertas duplicadas.
- **⏱️ Agendamento Inteligente**: Executa tarefas automaticamente a cada 5 minutos.
- **🛡️ Resiliência**: Implementa lógica de *retry* (tentativas) para lidar com limites da API do Telegram (Rate Limiting).

---

## 🛠️ Arquitetura

O projeto segue os princípios da **Clean Architecture** (Arquitetura Limpa), separando as responsabilidades em camadas:

- **Application**: Contém os casos de uso (`UseCase`) e regras de negócio.
- **Domain**: Define as entidades e interfaces (Portas).
- **Infrastructure**: Implementa os adaptadores para serviços externos (Telegram, Mercado Livre) e persistência (Banco de Dados).

---

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior
- Conta no Telegram e um Bot criado via @BotFather

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/shadowpromocoes-bot.git
cd shadowpromocoes-bot
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install requests schedule python-dotenv
```

### 4. Configuração do Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais:

```env
TELEGRAM_TOKEN=seu_token_aqui
TELEGRAM_CHANNEL=@seu_canal_aqui
```

### 5. Executando o Bot

```bash
python main.py
```

O bot iniciará o agendador e verificará novas ofertas a cada 5 minutos.

---

## 📂 Estrutura do Projeto

```
shadowpromocoes-bot/
├── application/          # Regras de negócio e Casos de Uso
├── infrastructure/       # Adaptadores (Telegram, DB, APIs)
├── main.py               # Ponto de entrada da aplicação
├── data.db               # Banco de dados SQLite
└── .env                  # Variáveis de ambiente
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests*.

---

## 📝 Licença

Este projeto está sob a licença MIT.
