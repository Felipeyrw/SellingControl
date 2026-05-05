# SellingControl

<p align="center">
  <strong>App de controle de vendas - sistema online</strong>
</p>

---

## 📋 Visão Geral

Um app simples para gerenciar o dia-dia de um vendedor com fornecedores, alimentos vendidos, adicionar amizades para acompanhar vendas, e o cadastro de vendas.

---
## 🚀 Funcionalidades
- 🚪 **Login/Cadastro** - Entrada por login ou cadastro no firebase, protegendo as contas.
- 💰 **Vendas** - Cadastro das vendas com fornecedores, alimentos e preços
- 👥 **Vendedores** - Cadastro de vendedores e acompanhamento de suas vendas
- ➡️ **Ver Vendas** - Acompanhar as suas vendas e de outros vendedores

---

## 🛠️ Tecnologias

| Categoria | Tecnologia |
|-----------|------------|
| Framework | Kivy |
| Banco de dados | FIREBASE |

---

## 📁 Estrutura de Arquivos

```
lib/
├── main.py                  # Entry point
├── myfirebase.py            # Integração com firebase
├── telas.py                 # Definição de telas no python
├── main.kv                  # Definição de telas no kivy
├── botoes.py                # Botões Utils
├── refresh_token.py         # Refresh Token ( Login automático pela sessão já validada )
├── icones/                  # Ícones usados no app
├── kv/                      # Lógica das telas
             
```
## 📄 Licença

MIT LICENSE
