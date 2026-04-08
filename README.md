# MViP — Metodologia de Viabilidade Paramétrica

Aplicação standalone em Python (Flask + frontend HTML/JS) para estudo de viabilidade paramétrica sem dependência de Rhino/Grasshopper.

## Funcionalidades implementadas

- Interface em abas:
  - Terreno & Urbanismo
  - Volumetria
  - Conformidade
  - Relatório
- Busca de lote por código (stub): `LOTE-001` e `LOTE-002`
  - Preenchimento automático de parâmetros urbanísticos
  - Carregamento automático do polígono do terreno (GeoJSON)
- Ajustes em tempo real por sliders:
  - Pavimentos
  - Pé-direito
  - Recuos frontal/lateral/fundos
- Geração paramétrica de volumetria simplificada com Shapely
- Representação do envelope volumétrico direto na tela (SVG)
- Gráfico comparativo (área construída × área do terreno) via Matplotlib
- Verificação de conformidade urbanística + checklist IT 08 (simplificado)
- Relatórios e exportações: PDF, PNG e DWG
- Persistência local com SQLite e CRUD de projetos

## Execução

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abra: `http://127.0.0.1:5000`

## Fluxo recomendado para teste

1. Digite um lote no campo **Buscar lote** (ex.: `LOTE-001`) e clique em **Buscar lote**.
2. Confira que o sistema preenche os parâmetros automaticamente.
3. Clique em **Processar volumetria paramétrica**.
4. Vá para a aba **Volumetria** e valide:
   - indicadores numéricos
   - envelope em SVG (visual instantâneo)
5. Ajuste os sliders (recuos/pavimentos/pé-direito) e observe atualização em tempo real.
6. Na aba **Relatório**, gere os arquivos e baixe PDF/DWG/PNG.

## Testes automatizados

```bash
pytest -q
```

## Dica de troubleshooting (volumetria não aparece)

- Se recuos estiverem muito altos para o tamanho do terreno, o envelope pode ficar vazio.
- Reduza recuos ou use o lote `LOTE-001` para validar o fluxo inicial.
- Verifique o console do navegador (`F12`) para erros de JavaScript.
