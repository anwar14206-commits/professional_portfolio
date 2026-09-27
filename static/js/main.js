/**
 * main.js - Core UI Interactions, AJAX Contact Form & Ambient Audio Engine
 */

(function () {
  // Contact Form AJAX Handler
  const contactForm = document.getElementById('cinematic-contact-form');
  const toast = document.getElementById('cinematic-toast');
  const toastMsg = document.getElementById('toast-message');

  function showToast(message, type = 'success') {
    if (!toast) return;
    toastMsg.textContent = message;
    toast.className = `cinematic-toast show ${type}`;
    setTimeout(() => {
      toast.classList.remove('show');
    }, 4500);
  }

  if (contactForm) {
    contactForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : 'Send Message';
      
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Transmitting...';
      }

      const formData = new FormData(contactForm);

      try {
        const response = await fetch('/contact', {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          showToast(data.message || 'Your message has entered the sanctuary. Thank you!', 'success');
          contactForm.reset();
        } else {
          showToast(data.message || 'Could not send message. Please try again.', 'error');
        }
      } catch (err) {
        // Fallback to standard submit if fetch fails
        contactForm.submit();
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalText;
        }
      }
    });
  }

  // Optional Ambient Atmosphere Synthesizer (Web Audio API)
  const soundToggleBtn = document.getElementById('ambient-sound-toggle');
  let audioCtx = null;
  let osc1 = null;
  let osc2 = null;
  let gainNode = null;
  let isPlaying = false;

  function initAmbientAudio() {
    if (audioCtx) return;
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();

      // Dual warm low-frequency drone oscillators
      osc1 = audioCtx.createOscillator();
      osc2 = audioCtx.createOscillator();
      const filter = audioCtx.createBiquadFilter();
      gainNode = audioCtx.createGain();

      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(55, audioCtx.currentTime); // A1 note

      osc2.type = 'triangle';
      osc2.frequency.setValueAtTime(110, audioCtx.currentTime); // A2 note

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(180, audioCtx.currentTime);

      gainNode.gain.setValueAtTime(0.001, audioCtx.currentTime);

      osc1.connect(filter);
      osc2.connect(filter);
      filter.connect(gainNode);
      gainNode.connect(audioCtx.destination);

      osc1.start();
      osc2.start();
    } catch (e) {
      console.warn('Web Audio not supported or blocked');
    }
  }

  if (soundToggleBtn) {
    soundToggleBtn.addEventListener('click', function () {
      if (!isPlaying) {
        initAmbientAudio();
        if (audioCtx && audioCtx.state === 'suspended') {
          audioCtx.resume();
        }
        if (gainNode) {
          gainNode.gain.setTargetAtTime(0.04, audioCtx.currentTime, 0.5);
        }
        isPlaying = true;
        soundToggleBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
        soundToggleBtn.style.color = '#38bdf8';
        showToast('Atmospheric drone activated', 'info');
      } else {
        if (gainNode && audioCtx) {
          gainNode.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.5);
        }
        isPlaying = false;
        soundToggleBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
        soundToggleBtn.style.color = '';
      }
    });
  }

  // Smooth scroll links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href').substring(1);
      if (!targetId) return;
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
})();
