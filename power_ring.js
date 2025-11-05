export async function createEnergyRing(
  canvas,
  jsonPath = 'data/energy_stream.json'
) {
  if (!(canvas instanceof HTMLCanvasElement)) {
    throw new TypeError('Canvas element required');
  }

  const ctx = canvas.getContext('2d');
  const { width: W, height: H } = canvas;
  const cx = W / 2;
  const cy = H / 2;
  const r = Math.min(W, H) * 0.35;

  let energy = [];
  try {
    const res = await fetch(jsonPath, { cache: 'no-store' });
    if (!res.ok) {
      throw new Error(`Failed to fetch ${jsonPath}: ${res.status}`);
    }
    const data = await res.json();
    energy = Array.isArray(data.energy) ? data.energy : [];
  } catch (err) {
    console.warn('Falling back to synthetic energy stream:', err);
    for (let i = 0; i < 1200; i += 1) {
      energy.push(0.5 + 0.5 * Math.sin(i * 0.05));
    }
  }

  if (energy.length === 0) {
    energy = [0.5];
  }

  let frame = 0;

  const lerp = (a, b, t) => a + (b - a) * t;

  const energyToRGB = (e) => {
    if (e < 0.33) {
      return `rgb(${Math.round(50 + 100 * e)}, ${255 - Math.round(80 * e)}, 255)`;
    }
    if (e < 0.66) {
      return `rgb(${150 + Math.round(100 * e)}, 0, 255)`;
    }
    return `rgb(255, ${50 + Math.round(100 * (1 - e))}, ${200 + Math.round(55 * e)})`;
  };

  function draw() {
    const e = energy[frame % energy.length];
    const pulse = 1 + 0.03 * Math.sin(frame * 0.5) * (0.5 + e);
    const color = energyToRGB(e);

    ctx.clearRect(0, 0, W, H);

    ctx.save();
    const vibration = Math.sin(frame * 0.4) * e * 3;
    ctx.translate(vibration, -vibration);

    ctx.save();
    const grad = ctx.createRadialGradient(cx, cy, r * 0.4, cx, cy, r * 1.2);
    grad.addColorStop(0, color);
    grad.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = grad;
    ctx.globalAlpha = 0.35 + 0.35 * e;
    ctx.beginPath();
    ctx.arc(cx, cy, r * 1.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    ctx.lineWidth = lerp(6, 14, e);
    ctx.strokeStyle = color;
    ctx.shadowColor = color;
    ctx.shadowBlur = lerp(10, 40, e);
    ctx.beginPath();
    ctx.arc(cx, cy, r * pulse, 0, Math.PI * 2);
    ctx.stroke();

    const spokes = 24;
    ctx.lineWidth = 2;
    ctx.strokeStyle = color;
    for (let k = 0; k < spokes; k += 1) {
      const a = (k / spokes) * Math.PI * 2 + frame * 0.02;
      const inner = r * 0.78;
      const outer = r * 1.05 + 6 * e;
      ctx.beginPath();
      ctx.moveTo(cx + inner * Math.cos(a), cy + inner * Math.sin(a));
      ctx.lineTo(cx + outer * Math.cos(a), cy + outer * Math.sin(a));
      ctx.stroke();
    }

    const bar = document.getElementById('bar');
    if (bar) {
      bar.style.width = `${(e * 100).toFixed(1)}%`;
    }

    frame += 1;
    ctx.restore();
    requestAnimationFrame(draw);
  }

  draw();
}
