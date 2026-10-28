const button = document.querySelector('#soundToggle');
let audioContext, hum, gain;

function startSound(){
  audioContext = audioContext || new (window.AudioContext || window.webkitAudioContext)();
  hum = audioContext.createOscillator();
  gain = audioContext.createGain();
  hum.type = 'sine'; hum.frequency.value = 48; gain.gain.value = 0;
  hum.connect(gain).connect(audioContext.destination); hum.start();
  gain.gain.linearRampToValueAtTime(.018, audioContext.currentTime + 1.4);
}
function stopSound(){
  if(!gain) return;
  gain.gain.linearRampToValueAtTime(0, audioContext.currentTime + .4);
  setTimeout(()=>{ if(hum){ hum.stop(); hum=null; } },450);
}
button.addEventListener('click',()=>{
  const active = button.getAttribute('aria-pressed') !== 'true';
  button.setAttribute('aria-pressed', String(active));
  button.querySelector('b').textContent = active ? 'On' : 'Off';
  active ? startSound() : stopSound();
});
