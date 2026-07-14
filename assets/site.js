(() => {
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('siteNav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.hasAttribute('data-open');
      if (open) nav.removeAttribute('data-open');
      else nav.setAttribute('data-open', '');
      toggle.setAttribute('aria-expanded', String(!open));
    });
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) {
        nav.removeAttribute('data-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Only one nav dropdown open at a time; close on outside click
  const groups = Array.from(document.querySelectorAll('.nav-group'));
  groups.forEach((group) => {
    group.addEventListener('toggle', () => {
      if (group.open) groups.forEach((g) => { if (g !== group) g.open = false; });
    });
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.nav-group')) {
      groups.forEach((g) => { g.open = false; });
    }
  });

  // Sticky call CTA: fade in once the hero has scrolled out of view
  const stickyCta = document.querySelector('.sticky-cta');
  if (stickyCta) {
    const hero = document.querySelector('.hero, .split-hero');
    const show = (on) => stickyCta.classList.toggle('show', on);
    if (hero && 'IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => {
        show(!entry.isIntersecting && entry.boundingClientRect.top < 0);
      }).observe(hero);
    } else {
      // Pages without a hero (e.g. contact): show after a bit of scrolling
      const onScroll = () => show(window.scrollY > 400);
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  }

  async function submitForm(form, msgElement) {
    const honeypot = form.querySelector('input[name="_gotcha"]');
    if (honeypot && honeypot.value) return;

    const formData = new FormData(form);
    msgElement.textContent = 'Submitting...';
    msgElement.className = 'form-msg';

    try {
      const response = await fetch(form.action, {
        method: form.method || 'POST',
        body: formData,
        headers: { Accept: 'application/json' }
      });

      if (response.ok) {
        msgElement.textContent = 'Message sent! A team member will reach out shortly.';
        msgElement.className = 'form-msg ok';
        form.reset();
        return;
      }

      const data = await response.json().catch(() => ({}));
      msgElement.textContent = data && data.errors && data.errors.length
        ? data.errors.map((error) => error.message).join(', ')
        : 'Could not send. Please call (561) 254-0241';
      msgElement.className = 'form-msg err';
    } catch (error) {
      msgElement.textContent = 'Could not send. Please call (561) 254-0241';
      msgElement.className = 'form-msg err';
    }
  }

  document.querySelectorAll('form[data-formspree-form]').forEach((form) => {
    const msg = form.querySelector('[data-form-message]');
    if (!msg || form.dataset.bound === 'true') return;
    form.dataset.bound = 'true';
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      await submitForm(form, msg);
    });
  });

  document.querySelectorAll('[data-prefill]').forEach((element) => {
    element.addEventListener('click', () => {
      const message = element.getAttribute('data-prefill');
      const field = document.querySelector('form[data-formspree-form] textarea[name="message"]');
      if (message && field) field.value = message;
    });
  });
})();
