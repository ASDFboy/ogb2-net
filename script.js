function playCrtOff() {
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  if (!AudioCtx) return;
  const ctx = new AudioCtx();
  const now = ctx.currentTime;
  const toneEnd = 0.4;

  const osc = ctx.createOscillator();
  osc.type = "sine";
  const oscGain = ctx.createGain();
  osc.connect(oscGain).connect(ctx.destination);
  osc.frequency.setValueAtTime(1400, now);
  osc.frequency.exponentialRampToValueAtTime(35, now + toneEnd);
  oscGain.gain.setValueAtTime(0.25, now);
  oscGain.gain.exponentialRampToValueAtTime(0.0001, now + toneEnd);
  osc.start(now);
  osc.stop(now + toneEnd);

  const clickBuffer = ctx.createBuffer(1, ctx.sampleRate * 0.02, ctx.sampleRate);
  const clickData = clickBuffer.getChannelData(0);
  for (let i = 0; i < clickData.length; i++) clickData[i] = Math.random() * 2 - 1;
  const click = ctx.createBufferSource();
  click.buffer = clickBuffer;
  const clickGain = ctx.createGain();
  click.connect(clickGain).connect(ctx.destination);
  clickGain.gain.setValueAtTime(0.4, now + toneEnd);
  clickGain.gain.exponentialRampToValueAtTime(0.0001, now + toneEnd + 0.05);
  click.start(now + toneEnd);

  setTimeout(() => ctx.close(), (toneEnd + 0.08) * 1000);
}

const powerBtn = document.getElementById("power-btn");
if (powerBtn) {
  powerBtn.addEventListener("click", (event) => {
    event.preventDefault();
    playCrtOff();
    document.body.classList.add("crt-off");
    setTimeout(() => { window.location.href = powerBtn.href; }, 480);
  });
}
