# Publicação e atualização

## O que está publicado

O README é a página de apresentação do projeto. O PDF pode ser aberto ou baixado pelo link relativo no README, e o Markdown permite ler e revisar o texto diretamente no GitHub. Não é necessário ativar GitHub Pages.

## Estrutura

```text
README.md
assets/images/capa.jpg
ebook/seu-dinheiro-em-ordem.md
ebook/seu-dinheiro-em-ordem.pdf
prompts/leonardo-ai.md
docs/desafio-original.md
docs/publicacao.md
scripts/build_ebook.py
requirements.txt
```

Os exemplos originais do laboratório permanecem em `exemplos/`.

## Editar o texto e gerar o PDF

1. Edite `ebook/seu-dinheiro-em-ordem.md`. O marcador `<!-- page -->` inicia uma nova página. O primeiro bloco corresponde à capa; os seguintes compõem o conteúdo.
2. Use Python 3.10 ou superior e instale as dependências: `python -m pip install -r requirements.txt`.
3. Disponibilize Arial no Windows ou DejaVu Sans no Linux.
4. Execute `python scripts/build_ebook.py` na cópia local do repositório.
5. Confira o PDF visualmente. Se o conteúdo ultrapassar uma página, reduza ou redistribua o texto e atualize o sumário. O gerador interrompe com erro quando há páginas excedentes.
6. Envie o Markdown e o PDF atualizados no mesmo commit para manter as versões alinhadas.

O gerador usa apenas arquivos locais e não envia dados para serviços de IA.

## Adicionar ilustrações internas depois

Salve as imagens aprovadas em `assets/images/`, com nomes como `01-abertura.jpg`, `02-diagnostico.jpg`, `03-orcamento.jpg`, `04-dividas.jpg`, `05-reserva.jpg`, `06-metas.jpg` e `07-rotina.jpg`.

Adicionar o arquivo à pasta não o insere automaticamente no PDF. A versão atual do gerador aplica somente a capa. Para uma edição ilustrada, será necessário incluir as imagens na diagramação, rever as quebras de página e conferir novamente o sumário e o PDF. Atualize também os créditos e o status no README.

## Conferência antes de uma nova edição

- Verificar cálculos, linguagem, fontes e datas.
- Conferir título, acentos, margens, tabelas e números de página.
- Abrir os links locais e externos.
- Manter os créditos das ferramentas efetivamente utilizadas.
- Publicar apenas fichas em branco; nunca dados financeiros pessoais.

## Entrega na DIO

O endereço para entregar o projeto é o do fork: https://github.com/MarcosSlv/lab-natty-or-not. A submissão na plataforma da DIO é uma etapa separada da publicação no GitHub.
