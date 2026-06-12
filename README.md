# 🌱 CarbonTrack PME

78% das PMEs nunca mediram suas emissões. Partindo disso, nosso sistema surge com o objetivo de auxiliar gestores de pequenas e médias empresas na tomada de decisões baseada em dados. 

O projeto permite cadastrar empresas, fontes de emissão, registrar consumos mensais e calcular automaticamente emissões em tCO₂e utilizando GHG Protocol e fatores MCTI.

---
## Sobre o projeto

Desenvolvido a partir de um desafio da disciplina de Projetos 1 do curso de Sistemas de Informação, nossa solução propõe uma alternativa para as PMEs brasileiras que nunca mediram suas emissões de carbono. Sem dados, não conseguem comprovar redução para bancos, editais e clientes — e ficam de fora de linhas de crédito verde e programas de fomento como o Sebrae Verde e o BNDES.

Baseado em cadastro de empresas e fontes de emissão, a plataforma registra consumos mensais, calcula automaticamente as toneladas de CO₂ equivalente (tCO₂e) usando o GHG Protocol com fatores oficiais do MCTI. 

## Tecnologias Utilizadas

- Python;
- SQLite;
- Git & GitHub;

---

## Funcionalidades

### CRUD completo

- Cadastro de empresas;
- Cadastro de fontes de emissão;
- Registro de consumo mensal;
- Atualização de dados;
- Desativação de fontes;
- Consulta histórica;
- Exportação de relatórios.

### Base legal e metodológica

- GHG Protocol — metodologia de inventário de emissões de carbono
- Fatores MCTI — fatores de emissão oficiais do Ministério de Ciência e Tecnologia e Inovação
- Lei 15.042/2024 — legislação brasileira de conformidade para relatórios de emissões

## 📖 Manual do Usuário

> Sistema de terminal para gestão de emissões de carbono em pequenas e médias empresas.  
> Não é necessário conhecimento técnico — basta seguir os menus na tela.

---

### ▶️ Como executar o sistema

**Pré-requisito:** Python 3.10 ou superior instalado.

```bash
python main.py
```

O banco de dados (`carbontrack.db`) é criado automaticamente na primeira execução. Nenhuma instalação adicional é necessária.

---

### 🗺️ Visão geral dos menus

O sistema é organizado em três áreas principais, acessadas pelo menu inicial:

```
[1] Empresa
[2] Fontes de Emissão
[3] Consumo e Relatórios
[0] Sair
```

---

### 🏢 1. Empresa

#### Cadastrar empresa
Informe os dados da sua empresa uma única vez:

| Campo | Exemplo |
|---|---|
| Razão social | Gráfica Nordeste Ltda |
| CNPJ | 12.345.678/0001-99 |
| Setor | Indústria |
| Meta anual de tCO₂e | 50.0 (opcional — pressione Enter para pular) |

> ⚠️ O sistema impede o cadastro de CNPJs duplicados automaticamente.

#### Editar ou visualizar dados
Selecione a empresa pelo ID exibido na listagem e altere os campos desejados.

---

### 🏭 2. Fontes de Emissão

Uma **fonte de emissão** é qualquer atividade da empresa que gera carbono — como consumo de energia elétrica, uso de veículos a diesel ou geração de resíduos.

#### Cadastrar fonte
Informe:

| Campo | Opções disponíveis |
|---|---|
| Nome | Qualquer nome descritivo (ex: "Frota de entregas") |
| Tipo | `energia_eletrica`, `diesel`, `gasolina`, `etanol`, `glp`, `residuos` |
| Unidade | Definida automaticamente pelo tipo escolhido |

> 💡 O tipo precisa ser exatamente um dos valores listados acima — ele determina o fator de emissão usado nos cálculos.

#### Listar fontes
Exibe todas as fontes ativas da empresa selecionada com seus IDs.

#### Editar fonte
Selecione pelo ID e altere nome, tipo ou unidade.

#### Desativar fonte
A fonte é **desativada** (não apagada) — o histórico de consumo vinculado a ela é preservado para relatórios futuros.

---

### 📊 3. Consumo e Relatórios

#### Registrar consumo mensal
Para cada fonte de emissão, registre o consumo do mês:

| Campo | Exemplo |
|---|---|
| Fonte | Selecione pelo ID |
| Quantidade | 1500.0 |
| Mês de referência | 5 (maio) |
| Ano de referência | 2025 |

Após confirmar, o sistema calcula e exibe automaticamente o valor em **tCO₂e** usando os fatores oficiais do MCTI 2025 / GHG Protocol.

> ⚠️ Não é possível registrar dois consumos para a mesma fonte no mesmo mês/ano. Caso precise corrigir, utilize a opção de editar registro.

> ⚠️ O sistema recusa valores negativos ou zerados e alerta sobre valores muito discrepantes em relação ao histórico da fonte.

#### Exportar relatório (.csv)
Gera um arquivo `.csv` na pasta do projeto com todo o histórico de consumo e emissões. O arquivo pode ser aberto no Excel ou Google Sheets.

---

### 🔢 Fatores de emissão utilizados

| Tipo de fonte | Fator | Unidade de entrada |
|---|---|---|
| Energia elétrica | 0,0289 tCO₂e | por MWh |
| Diesel | 0,002603 tCO₂e | por litro |
| Gasolina | 0,002212 tCO₂e | por litro |
| Etanol | 0,001457 tCO₂e | por litro |
| GLP | 0,001578 tCO₂e | por kg |
| Resíduos | 0,5 tCO₂e | por tonelada |

> Fonte: MCTI 2025 e GHG Protocol Brasil.

---

### ❓ Dúvidas frequentes

**O sistema apagou minha fonte quando desativei?**  
Não. A desativação apenas oculta a fonte dos menus — o histórico de consumo continua salvo no banco de dados.

**Posso usar o sistema em Mac ou Linux?**  
Sim. O sistema é compatível com Windows, Mac e Linux.

**Onde fica o banco de dados?**  
O arquivo `carbontrack.db` é criado automaticamente na mesma pasta do `main.py`. Não o apague — ele contém todos os seus dados.

**Esqueci o ID da minha empresa/fonte. Como vejo?**  
Use as opções de listagem nos menus de Empresa e Fontes de Emissão — os IDs são sempre exibidos.

---

## Equipe
- [Gabriel Salvador](https://github.com/Gabriel-Salvador-1) 
- [Jullya Medeiros](https://github.com/juuvmed)
- [Lívia Buonora](https://github.com/liviabuonora)
- [Marcos Vinícius](https://github.com/marcos-felipe17) 
- [Rafael Gurgel](https://github.com/RafaelGMedeiros) 
- [Vinícius Machado](https://github.com/vml2-lab) 


---

## 🔗 Links Úteis
- [Google Sites](https://sites.google.com/cesar.school/projeto1-grupo1-si-2026-1/sr2)
- [Notion do Projeto](https://heathered-team-4c3.notion.site/Cronograma_CarbonTrack_PME-360288871b3080c2a025ecbf4dad7282)

Projetos 1 - CESAR School - SI (2026.1)
