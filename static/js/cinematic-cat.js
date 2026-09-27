/**
 * cinematic-cat.js - Scroll-Controlled Black Cat Cinematic Journey Engine
 * Manages frame crossfading, camera perspective, glowing eye luminescence,
 * and seamless scroll timeline synchronization.
 */

(function () {
  // Cat Frames
  const frames = [
    document.getElementById('cat-frame-1'), // Standing (0%)
    document.getElementById('cat-frame-2'), // Turning Head (20%)
    document.getElementById('cat-frame-3'), // Walking (40%)
    document.getElementById('cat-frame-4'), // Prowling / Approaching (60-80%)
    document.getElementById('cat-frame-5')  // Resting on Dais (100%)
  ];

  const catRig = document.getElementById('cat-stage-rig');
  const eyeSpots = document.querySelectorAll('.eye-glow-spot');
  const hudProgressBar = document.getElementById('hud-progress-bar');
  const hudDots = document.querySelectorAll('.hud-dot');
  const chapters = document.querySelectorAll('.cinematic-chapter');
  const navLinks = document.querySelectorAll('.nav-link');

  let currentFrameIndex = 0;
  let targetProgress = 0;
  let currentProgress = 0;
  let mouseX = 0;
  let mouseY = 0;

  // Frame thresholds according to the requested sequence:
  // 0% -> standing
  // 20% -> turns head
  // 40% -> begins walking
  // 60-80% -> camera follows / approaches project section
  // 100% -> final scene / contact sanctuary
  function getFrameIndex(progress) {
    if (progress < 0.16) return 0;
    if (progress < 0.36) return 1;
    if (progress < 0.56) return 2;
    if (progress < 0.82) return 3;
    return 4;
  }

  // Calculate cat rig cinematic transform based on scroll progress
  function calculateRigTransform(progress) {
    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      // Simplified mobile positioning so text is 100% accessible
      return {
        x: 0,
        y: progress > 0.8 ? 10 : -5,
        scale: 0.85,
        opacity: progress > 0.85 ? 0.35 : 0.45
      };
    }

    let x = 0;
    let y = 0;
    let scale = 1;
    let opacity = 1;

    if (progress < 0.18) {
      // 0%: Standing on right side of hero
      const t = progress / 0.18;
      x = 18 - t * 2;
      y = 0;
      scale = 1.02;
    } else if (progress < 0.38) {
      // 20%: Turning head, glide towards left for About section
      const t = (progress - 0.18) / 0.20;
      x = 16 - t * 36; // ends at -20vw
      y = t * 4;
      scale = 0.98;
    } else if (progress < 0.58) {
      // 40%: Walking, moves to right for Skills section
      const t = (progress - 0.38) / 0.20;
      x = -20 + t * 42; // ends at +22vw
      y = 4 - t * 6;
      scale = 1.0;
    } else if (progress < 0.84) {
      // 60-80%: Approaching Projects, low prowl centered
      const t = (progress - 0.58) / 0.26;
      x = 22 - t * 22; // centers
      y = -2 + t * 14;
      scale = 1.0 + t * 0.12;
    } else {
      // 100%: Final stone dais at contact
      const t = (progress - 0.84) / 0.16;
      x = 0 - t * 24; // left-hand dais
      y = 12 - t * 6;
      scale = 1.02;
    }

    return { x, y, scale, opacity };
  }

  function updateVisuals() {
    // Smooth progress interpolation
    currentProgress += (targetProgress - currentProgress) * 0.1;

    // Determine active frame
    const newFrameIdx = getFrameIndex(currentProgress);
    if (newFrameIdx !== currentFrameIndex) {
      frames.forEach((f, idx) => {
        if (!f) return;
        if (idx === newFrameIdx) {
          f.classList.add('active');
        } else {
          f.classList.remove('active');
        }
      });
      currentFrameIndex = newFrameIdx;
    }

    // Apply smooth rig motion
    if (catRig) {
      const transform = calculateRigTransform(currentProgress);
      catRig.style.transform = `translate3d(${transform.x}vw, ${transform.y}vh, 0) scale(${transform.scale})`;
      catRig.style.opacity = transform.opacity;
    }

    // Update HUD Progress
    if (hudProgressBar) {
      hudProgressBar.style.height = `${currentProgress * 100}%`;
    }

    // Update active HUD dot and nav links
    const activeChapterIdx = Math.min(
      chapters.length - 1,
      Math.floor(currentProgress * (chapters.length))
    );

    hudDots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === activeChapterIdx);
    });

    navLinks.forEach((link, idx) => {
      link.classList.toggle('active', idx === activeChapterIdx);
    });

    requestAnimationFrame(updateVisuals);
  }

  // Scroll listener
  function onScroll() {
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    targetProgress = docHeight > 0 ? Math.max(0, Math.min(1, window.scrollY / docHeight)) : 0;
  }

  // Subtle Mouse Tracking for Glowing Cat Eyes
  function onMouseMove(e) {
    if (window.innerWidth <= 768) return;
    const normX = (e.clientX / window.innerWidth - 0.5) * 6;
    const normY = (e.clientY / window.innerHeight - 0.5) * 6;

    eyeSpots.forEach(eye => {
      eye.style.transform = `translate(${normX}px, ${normY}px)`;
    });
  }

  // Click on HUD dots to glide to chapter
  hudDots.forEach(dot => {
    dot.addEventListener('click', () => {
      const targetId = dot.getAttribute('data-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Preload cat images to prevent flickering
  function preloadImages() {
    frames.forEach(frame => {
      if (frame && frame.src) {
        const img = new Image();
        img.src = frame.src;
      }
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('mousemove', onMouseMove, { passive: true });
  window.addEventListener('resize', onScroll);

  preloadImages();
  onScroll();
  requestAnimationFrame(updateVisuals);
})();
