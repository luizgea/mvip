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

## Observações

- A integração WFS/WMS da PBH está preparada como stub (`mvip/pbh.py`) para facilitar ligação com endpoints oficiais.
- O export IFC está planejado em `roadmap` e pode ser implementado via IfcOpenShell em etapa futura.
