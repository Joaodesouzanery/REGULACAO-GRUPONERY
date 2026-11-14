# Acordo de Tratamento de Dados Pessoais (DPA) — MODELO

> **MODELO PARA REVISÃO POR ADVOGADO.** Não é aconselhamento jurídico. Lei 13.709/2018 (LGPD); Resolução CD/ANPD 15/2024 (incidentes). Bases conferidas em 14/11/2026.

## 1. Papéis (LGPD, art. 5º, VI e VII; arts. 37 a 40)
| Dado | Controlador | Operador |
|---|---|---|
| Dados de agentes públicos (diretores, superintendentes) em reuniões, atas, DOU e Senado | Grupo Nery (define finalidade e meios da base) | — |
| Dados do cliente final (processos, CNPJ, intimações, contatos) | Cliente final | Parceiro e Grupo Nery (suboperador) |
| Dados de contato comercial entre as partes | cada parte, para si | — |

## 2. Bases legais
2.1. **Agentes públicos:** dados de acesso público tratados conforme finalidade, boa-fé e interesse público que justificaram a disponibilização (art. 7º, §3º); dados tornados manifestamente públicos (art. 7º, §4º), resguardados os direitos do titular; **legítimo interesse** (art. 7º, IX, e art. 10), com teste de proporcionalidade documentado. Escopo restrito à **atuação na função pública** (votos, falas em sessão, mandato, formação oficial). Nada de vida privada, sem rótulos pessoais, sem dados sensíveis (art. 11).
2.2. **Dados do cliente:** execução de contrato (art. 7º, V) e legítimo interesse (art. 7º, IX), conforme instruções do controlador (art. 39).

## 3. Obrigações do operador (arts. 39, 46 a 49)
3.1. Tratar só conforme instruções escritas do controlador e para prestar o serviço.
3.2. **Segurança:** dados do cliente **fora do repositório principal** (pasta `clientes/` no `.gitignore` ou repositório privado separado); acesso restrito por pessoa, autenticação em dois fatores, criptografia em trânsito e no armazenamento do provedor, cópia de segurança local, registro de operações (art. 37).
3.3. Confidencialidade de todos os que tiverem acesso.
3.4. Apoiar o controlador nos pedidos dos titulares (arts. 18 e 19) e em relatórios de impacto (art. 38).

## 4. Suboperadores
Autorizados: GitHub (repositório privado; não recebe dados do cliente), provedor de nuvem e ambiente de execução do assistente de IA usado no processamento, e-mail corporativo. Novo suboperador: aviso com 15 dias, com direito de oposição fundamentada. Transferência internacional conforme arts. 33 a 36 e regulamento da ANPD (Resolução CD/ANPD 19/2024, cláusulas-padrão), quando o provedor estiver fora do Brasil.

## 5. Incidentes de segurança
5.1. O operador avisa o controlador **em até 24 horas** após tomar ciência, com natureza, dados e titulares afetados, medidas e contato.
5.2. O controlador comunica à **ANPD** e aos titulares, quando o incidente puder gerar risco ou dano relevante, em **3 dias úteis** a contar da ciência de que dados pessoais foram afetados (LGPD, art. 48; Resolução CD/ANPD 15/2024, arts. 6º e 9º), podendo complementar em 20 dias úteis. Agentes de pequeno porte: prazos em dobro (Resolução CD/ANPD 2/2022).
5.3. Registro interno de todos os incidentes por 5 anos.

## 6. Retenção, devolução e eliminação
Dados do cliente mantidos durante o contrato; no término, devolvidos (PDF/CSV) e eliminados em até 30 dias, salvo obrigação legal (art. 16). Dados de agentes públicos da base: mantidos enquanto houver finalidade de análise da função pública, com revisão anual.

## 7. Encarregado
Grupo Nery: {{encarregado.nome}} — {{encarregado.email}} (art. 41).

## 8. Responsabilidade
Arts. 42 a 45 da LGPD; o operador responde solidariamente quando descumprir a lei ou as instruções lícitas do controlador (art. 42, §1º, I).
