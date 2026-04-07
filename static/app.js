const sampleGeojson = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {},
      geometry: {
        type: "Polygon",
        coordinates: [[
          [0, 0], [40, 0], [40, 30], [0, 30], [0, 0]
        ]]
      }
    }
  ]
};

document.getElementById("geojson").value = JSON.stringify(sampleGeojson, null, 2);

for (const btn of document.querySelectorAll(".tab")) {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach(x => x.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
  });
}

function payloadFromForm() {
  return {
    name: document.getElementById("name").value,
    typology: document.getElementById("typology").value,
    floors: Number(document.getElementById("floors").value),
    terrain_geojson: JSON.parse(document.getElementById("geojson").value),
    urban: {
      ca: Number(document.getElementById("ca").value),
      tdc: Number(document.getElementById("tdc").value),
      odc: Number(document.getElementById("odc").value),
      setback_front: Number(document.getElementById("setback_front").value),
      setback_side: Number(document.getElementById("setback_side").value),
      setback_back: Number(document.getElementById("setback_back").value),
      max_height: Number(document.getElementById("max_height").value),
      altimetry_min: Number(document.getElementById("altimetry_min").value),
      altimetry_max: Number(document.getElementById("altimetry_max").value),
      occupancy_rate_max: Number(document.getElementById("occupancy_rate_max").value),
    },
    scenarios: [
      { ca: Number(document.getElementById("ca").value) * 0.9, max_height: Number(document.getElementById("max_height").value) },
      { ca: Number(document.getElementById("ca").value) * 1.1, max_height: Number(document.getElementById("max_height").value) + 6, setback_back: Number(document.getElementById("setback_back").value) + 1 },
    ]
  };
}

function setCompliance(compliance) {
  const root = document.getElementById("compliance-result");
  root.innerHTML = "";

  const title = document.createElement("p");
  title.innerHTML = `Status geral: <span class="${compliance.overall_ok ? "ok" : "nok"}">${compliance.overall_ok ? "CONFORME" : "NÃO CONFORME"}</span>`;
  root.appendChild(title);

  for (const [name, item] of Object.entries(compliance.urban_checks)) {
    const p = document.createElement("p");
    p.innerHTML = `${name.toUpperCase()}: ${item.value} / limite ${item.limit} — <span class="${item.ok ? "ok" : "nok"}">${item.ok ? "OK" : "FALHA"}</span>`;
    root.appendChild(p);
  }

  const h = document.createElement("h3");
  h.textContent = "Checklist IT 08";
  root.appendChild(h);

  const ul = document.createElement("ul");
  for (const item of compliance.fire_checklist) {
    const li = document.createElement("li");
    li.innerHTML = `<span class="${item.ok ? "ok" : "nok"}">${item.ok ? "✔" : "✖"}</span> ${item.item} — ${item.note}`;
    ul.appendChild(li);
  }
  root.appendChild(ul);
}

document.getElementById("btn-pbh").addEventListener("click", async () => {
  const response = await fetch("/api/pbh", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lat: -19.92, lon: -43.94 }),
  });
  const data = await response.json();
  document.getElementById("pbh-result").textContent = JSON.stringify(data, null, 2);
});

document.getElementById("btn-analyze").addEventListener("click", async () => {
  const response = await fetch("/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payloadFromForm()),
  });
  const data = await response.json();

  document.getElementById("volume-result").innerHTML = `
    <p>Área do terreno: <b>${data.volume.terrain_area.toFixed(2)} m²</b></p>
    <p>Área edificável por pavimento: <b>${data.volume.max_floor_area.toFixed(2)} m²</b></p>
    <p>Área construída total: <b>${data.volume.gross_area.toFixed(2)} m²</b></p>
    <p>Altura utilizada: <b>${data.volume.used_height.toFixed(2)} m</b></p>
  `;

  setCompliance(data.compliance);
});

document.getElementById("btn-save").addEventListener("click", async () => {
  const response = await fetch("/api/projects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payloadFromForm()),
  });
  const data = await response.json();
  alert(`Projeto salvo com ID ${data.id}`);
  loadProjects();
});

async function loadProjects() {
  const response = await fetch("/api/projects");
  const projects = await response.json();
  const root = document.getElementById("projects");
  root.innerHTML = "<h3>Projetos salvos</h3>";
  const ul = document.createElement("ul");
  projects.forEach(p => {
    const li = document.createElement("li");
    li.textContent = `#${p.id} - ${p.name} (${p.created_at})`;
    ul.appendChild(li);
  });
  root.appendChild(ul);
}

document.getElementById("btn-export").addEventListener("click", async () => {
  const response = await fetch("/api/export", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payloadFromForm()),
  });
  const data = await response.json();

  const root = document.getElementById("export-result");
  root.innerHTML = `
    <p><a href="/api/download/${data.report_pdf}">Baixar relatório PDF</a></p>
    <p><a href="/api/download/${data.fire_pdf}">Baixar checklist incêndio</a></p>
    <p><a href="/api/download/${data.dwg}">Baixar DWG</a></p>
    <p><a href="/api/download/${data.volume_png}">Baixar imagem 3D</a></p>
    <p><a href="/api/download/${data.chart_png}">Baixar gráfico</a></p>
  `;

  document.getElementById("volume-preview").src = `/api/download/${data.volume_png}`;
  document.getElementById("chart-preview").src = `/api/download/${data.chart_png}`;
});

loadProjects();
