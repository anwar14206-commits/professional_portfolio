/**
 * particles.js - Lightweight Atmospheric Mist & Luminescent Dust Particle Canvas
 * Provides realistic volumetric atmosphere with zero external dependencies.
 */

(function () {
  const canvas = document.getElementById('ambient-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  let particles = [];
  const PARTICLE_COUNT = window.innerWidth < 768 ? 35 : 75;
  let scrollSpeedFactor = 1;
  let lastScrollY = window.scrollY;

  class MistParticle {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * width;
      this.y = initial ? Math.random() * height : height + Math.random() * 50;
      this.radius = Math.random() * 2.2 + 0.6;
      this.baseAlpha = Math.random() * 0.45 + 0.15;
      this.alpha = this.baseAlpha;
      this.speedY = -(Math.random() * 0.35 + 0.1);
      this.speedX = (Math.random() - 0.5) * 0.25;
      this.pulseSpeed = Math.random() * 0.02 + 0.008;
      this.pulseVal = Math.random() * Math.PI;
      // Cool cyan / starlight hue
      this.hue = Math.random() > 0.3 ? '56, 189, 248' : '147, 197, 253';
    }

    update() {
      this.pulseVal += this.pulseSpeed;
      this.alpha = this.baseAlpha + Math.sin(this.pulseVal) * 0.12;

      this.y += this.speedY * scrollSpeedFactor;
      this.x += this.speedX;

      if (this.y < -20 || this.x < -20 || this.x > width + 20) {
        this.reset();
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.hue}, ${Math.max(0, this.alpha)})`;
      ctx.shadowBlur = this.radius * 4;
      ctx.shadowColor = `rgba(${this.hue}, 0.8)`;
      ctx.fill();
    }
  }

  function init() {
    particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push(new MistParticle());
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    // Subtle dark mist gradient
    const grad = ctx.createRadialGradient(
      width * 0.5,
      height * 0.4,
      100,
      width * 0.5,
      height * 0.5,
      width * 0.8
    );
    grad.addColorStop(0, 'rgba(2, 6, 14, 0.0)');
    grad.addColorStop(1, 'rgba(5, 6, 8, 0.4)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw();
    }

    // Decay scroll speed factor back to 1
    scrollSpeedFactor += (1 - scrollSpeedFactor) * 0.08;

    requestAnimationFrame(render);
  }

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    init();
  });

  window.addEventListener('scroll', () => {
    const delta = Math.abs(window.scrollY - lastScrollY);
    scrollSpeedFactor = Math.min(3.5, 1 + delta * 0.04);
    lastScrollY = window.scrollY;
  }, { passive: true });

  init();
  render();
})();
