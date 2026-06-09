# ODYSSEY - Monitoramento Biológico Ambiental

## Unindo Visão Computacional e monitoramento ambiental preventivo

O ODYSSEY é uma solução desenvolvida em Python que utiliza Visão Computacional para monitorar o comportamento de espécies bioindicadoras e identificar possíveis riscos ambientais.

---

# Sobre o Projeto

O ODDYSEY é uma solução de monitoramento ambiental baseada em Visão Computacional que utiliza vídeos contendo canários para analisar padrões de comportamento coletivo e identificar possíveis situações de risco.

A proposta parte do princípio de que determinadas espécies podem atuar como bioindicadoras ambientais, apresentando alterações comportamentais diante de mudanças ou ameaças presentes no ambiente.

A solução combina:

* Detecção de aves utilizando YOLOv8;
* Processamento de vídeo utilizando OpenCV;
* Análise de movimentação coletiva;
* Simulação de dados ambientais provenientes de satélites;
* Sistema de classificação de risco ambiental.

A partir da correlação entre comportamento das aves, intensidade de movimento e dados ambientais simulados, o sistema classifica a situação monitorada em três estados:

* 🟢 NORMAL
* 🟡 SUSPEITO
* 🔴 ALERTA

O objetivo é demonstrar como diferentes fontes de informação podem ser combinadas para gerar alertas preventivos e auxiliar no monitoramento ambiental.

---

# 🎥 Demonstração da Solução

O vídeo abaixo apresenta o funcionamento completo do sistema ODYSSEY.

[▶ Assistir Demonstração](https://youtu.be/OVSkf2IT-R4)

### Funcionalidades apresentadas

* Detecção de aves utilizando YOLOv8;
* Processamento de vídeo com OpenCV;
* Monitoramento do comportamento coletivo dos canários;
* Simulação de dados ambientais via satélite;
* Geração automática de alertas ambientais;
* Painel de monitoramento em tempo real.

---

# Conexão com o Tema Espacial

O projeto possui inspiração em sistemas modernos de monitoramento ambiental que utilizam tecnologias espaciais para observar o planeta.

No protótipo atual, foram implementadas simulações de dados ambientais que representam informações que poderiam ser obtidas por satélites de observação da Terra, como:

* Detecção de focos de calor;
* Identificação de fumaça;
* Monitoramento de eventos ambientais.

A integração entre dados biológicos e ambientais permite uma análise mais confiável, reduzindo falsos alertas e aproximando a solução de cenários reais de monitoramento.

---

# Funcionamento da Solução

## 1. Captura de Vídeo

O sistema realiza a leitura de um vídeo contendo canários em uma área monitorada.

## 2. Detecção das Aves

Utilizando o modelo YOLOv8, o sistema identifica automaticamente as aves presentes em cada quadro do vídeo.

## 3. Análise de Movimento

O OpenCV é utilizado para comparar quadros consecutivos e medir o nível de movimentação coletiva das aves.

## 4. Simulação de Dados Satelitais

O sistema simula eventos ambientais como:

* Foco de calor;
* Presença de fumaça.

## 5. Classificação de Risco

A partir da correlação entre comportamento das aves, movimentação observada e dados ambientais, o sistema classifica o ambiente em três estados:

### 🟢 NORMAL

Condições dentro dos padrões esperados.

### 🟡 SUSPEITO

Movimentação anormal ou ocorrência de evento ambiental.

### 🔴 ALERTA

Combinação de alterações comportamentais e evidências ambientais que indicam um possível risco.

---

# Fluxo da Solução

```text
Vídeo
   ↓
Detecção de aves (YOLOv8)
   ↓
Análise de movimento (OpenCV)
   ↓
Dados ambientais simulados
   ↓
Correlação das informações
   ↓
Classificação do risco
   ↓
Painel de monitoramento
```

---

# Tecnologias Utilizadas

## Linguagem

* Python

## Bibliotecas

* OpenCV
* Ultralytics YOLO

## Técnicas Aplicadas

* Visão Computacional
* Detecção de Objetos
* Processamento de Imagens
* Análise de Movimento
* Máquina de Estados

---

# Bibliotecas Utilizadas

| Biblioteca       | Finalidade                       |
| ---------------- | -------------------------------- |
| OpenCV           | Processamento de vídeo e imagens |
| Ultralytics YOLO | Detecção automática das aves     |
| Time             | Controle temporal dos alertas    |

---

# Instalação e Execução

## Pré-requisitos

* Python 3.10 ou superior
* Git

## Clonar o Repositório

```bash
git clone https://github.com/ianny2003/Oddyssey-IoT-IoB.git

cd Oddyssey-IoT-IoB
```

## Instalar Dependências

```bash
pip install -r requirements.txt
```

## Executar o Projeto

```bash
python main.py
```

---

# Estrutura do Projeto

```text
ODDYSSEY/
│
├── main.py
├── requirements.txt
├── README.md
├── yolov8m.pt
├── yolov8n.pt
├── yolov8s.pt
└── canarios.mp4
```

---

# Integrantes

| Nome                               | RM       |
| ---------------------------------- | -------- |
| Ana Laura Torres Loureiro          | RM554375 |
| Murilo Cordeiro Ferreira           | RM556727 |
| Geronimo Augusto Nascimento Santos | RM557170 |
| Ianny Raquel Ferreira De Souza     | RM559096 |

---

FIAP • Global Solution • Engenharia de Software
