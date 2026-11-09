# Comandos do Mac (copiar e colar, um bloco por vez)

Abra o Terminal e entre na pasta do projeto:
```bash
cd ~/REGULACAO-GRUPONERY
```
Garanta o branch certo e o código mais novo:
```bash
git checkout claude/antt-directors-speeches-analysis-93r9hi && git pull --no-rebase -X theirs --no-edit
```
Se o pull reclamar de «unmerged files» ou «merge»:
```bash
git merge --abort; git rebase --abort; git fetch origin && git merge -X theirs origin/claude/antt-directors-speeches-analysis-93r9hi -m sincroniza
```

## Whisper (vídeos sem legenda) — deixe o Mac ligado
ANTT (as 4 reuniões de diretoria sem texto):
```bash
caffeinate -i bash pipeline/whisper_mac.sh
```
ANM (vídeos sem legenda da ANM):
```bash
caffeinate -i bash pipeline/whisper_mac.sh --agencia anm
```
Cada vídeo transcrito é enviado sozinho ao GitHub. Se aparecer «PUSH FALHOU», rode:
```bash
git push
```

## Coleta de vídeos novos (legendas)
```bash
caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh
```
```bash
caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh anm PLoP8nQ7f1EABonZ_nYkKU9xsGx6L6PjY8
```
```bash
caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh antaq @ANTAQ_oficial
```

## Conferir se subiu
```bash
git status && git log -3 --oneline && git push
```
Se `git log` mostrar commits seus que não estão no GitHub, o `git push` envia.

## DOU (posses) — uma vez, com cadastro gratuito em https://inlabs.in.gov.br
```bash
export INLABS_EMAIL='seu@email' INLABS_SENHA='sua_senha'
```
```bash
python3 pipeline/baixar_dou_mac.py && python3 pipeline/baixar_dou_mac.py --agencia anm && git add data/fontes_dou && git commit -m DOU && git push
```
