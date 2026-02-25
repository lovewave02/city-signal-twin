const hotspotEl = document.getElementById('hotspots');
const trendEl = document.getElementById('trend');

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      osm: {
        type: 'raster',
        tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: '&copy; OpenStreetMap contributors'
      }
    },
    layers: [{ id: 'osm', type: 'raster', source: 'osm' }]
  },
  center: [126.978, 37.566],
  zoom: 10.2
});

function colorByStress(v) {
  if (v >= 45) return '#bb2a1e';
  if (v >= 35) return '#de7a1f';
  return '#288f5a';
}

async function load() {
  const [signalsRes, hotspotsRes, trendRes] = await Promise.all([
    fetch('/signals'),
    fetch('/stress/hotspots?limit=5'),
    fetch('/stress/trend?hours=12')
  ]);
  const signals = await signalsRes.json();
  const hotspots = await hotspotsRes.json();
  const trend = await trendRes.json();

  hotspotEl.innerHTML = hotspots.hotspots
    .map(
      (x) =>
        `<li><strong>${x.name}</strong> — stress ${x.stress_index} (delay ${x.transit_delay_min}m, PM2.5 ${x.pm25})</li>`
    )
    .join('');

  const max = Math.max(...trend.points.map((p) => p.avg_stress_index));
  trendEl.innerHTML = trend.points
    .map((p) => {
      const h = Math.round((p.avg_stress_index / max) * 100);
      const label = new Date(p.ts).toISOString().slice(11, 16);
      return `<div class="bar" style="height:${h}%"><span>${label}</span></div>`;
    })
    .join('');

  map.on('load', () => {
    for (const area of signals.areas) {
      new maplibregl.Marker({ color: colorByStress(area.stress_index) })
        .setLngLat([area.lon, area.lat])
        .setPopup(
          new maplibregl.Popup({ offset: 20 }).setHTML(
            `<strong>${area.name}</strong><br/>Stress: ${area.stress_index}<br/>Delay: ${area.transit_delay_min}m<br/>PM2.5: ${area.pm25}`
          )
        )
        .addTo(map);
    }
  });
}

load().catch((e) => {
  console.error(e);
  hotspotEl.innerHTML = '<li>Failed to load signals.</li>';
});
