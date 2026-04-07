# MViP — Metodologia de Viabilidade Paramétrica

Aplicação standalone em Python (Flask + frontend HTML/JS) para estudo de viabilidade paramétrica sem dependência de Rhino/Grasshopper.

## Funcionalidades implementadas

- Interface em abas:
  - Terreno & Urbanismo
  - Volumetria
  - Conformidade
  - Relatório
- Entrada de dados com:
  - Importação de GeoJSON
  - Simulação de integração WFS/WMS PBH (stub configurável)
  - Parâmetros urbanísticos (CA, TDC, ODC, recuos, altura, cotas)
  - Tipologia e número de pavimentos
- Geração paramétrica de volumetria simplificada com Shapely
- Simulação de cenários múltiplos
- Gráfico comparativo (área construída × área do terreno) via Matplotlib
- Verificação de conformidade:
  - CA, TO, recuos e altura
  - Regras de segurança inspiradas na IT 08 CBMMG
- Relatórios e exportações:
  - PDF consolidado
  - Checklist de segurança em PDF
  - Imagem 3D básica em PNG
  - DWG simplificado via `ezdxf`
- Persistência local com SQLite e CRUD de projetos

## Estrutura

```text
mvip/
  app.py
  config.py
  requirements.txt
  tests/
    test_api_smoke.py
  mvip/
    models.py
    geometry.py
    compliance.py
    report.py
    exporters.py
    pbh.py
    storage.py
  templates/
    index.html
  static/
    app.js
    styles.css
```

## Execução

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abra: `http://127.0.0.1:5000`

## Como testar a aplicação

### 1) Teste manual da interface

1. Inicie o servidor com `python app.py`.
2. Acesse `http://127.0.0.1:5000`.
3. Na aba **Terreno & Urbanismo**, clique em **Processar volumetria paramétrica**.
4. Verifique resultados nas abas **Volumetria** e **Conformidade**.
5. Na aba **Relatório**, clique em **Gerar relatório PDF + DWG + PNG** e baixe os arquivos.

### 2) Teste automatizado (smoke)

Com ambiente virtual ativo e dependências instaladas:

```bash
pytest -q
```

Esse teste valida os endpoints principais:
- `POST /api/analyze`
- `POST /api/export`

### 3) Teste rápido via API (curl)

Com o servidor rodando:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Teste curl",
    "typology":"mista",
    "floors":6,
    "terrain_geojson":{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[0,0],[30,0],[30,20],[0,20],[0,0]]]}}]},
    "urban":{"ca":2.0,"tdc":0.0,"odc":0.0,"setback_front":3.0,"setback_side":2.0,"setback_back":3.0,"max_height":24.0,"altimetry_min":850.0,"altimetry_max":890.0,"occupancy_rate_max":0.6},
    "scenarios":[{"ca":1.8},{"ca":2.2,"max_height":30}]
  }'
```

## Observações

- A integração WFS/WMS da PBH está preparada como stub (`mvip/pbh.py`) para facilitar ligação com endpoints oficiais.
- O export IFC está planejado em `roadmap` e pode ser implementado via IfcOpenShell em etapa futura.
