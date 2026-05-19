(() => {
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;

      const target = document.querySelector(href);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  document.querySelectorAll('.navbar-collapse .nav-link, .navbar-collapse .dropdown-item').forEach((link) => {
    link.addEventListener('click', () => {
      if (link.classList.contains('dropdown-toggle')) return;

      const navbar = link.closest('.navbar-collapse');
      if (!navbar || !navbar.classList.contains('show') || !window.bootstrap) return;

      const collapse = window.bootstrap.Collapse.getOrCreateInstance(navbar, { toggle: false });
      collapse.hide();
    });
  });

  async function submitForm(form, msgElement) {
    const honeypot = form.querySelector('input[name="_gotcha"]');
    if (honeypot && honeypot.value) return;

    const formData = new FormData(form);
    msgElement.textContent = 'Submitting...';
    msgElement.className = 'small text-secondary mt-1';

    try {
      const response = await fetch(form.action, {
        method: form.method || 'POST',
        body: formData,
        headers: { Accept: 'application/json' }
      });

      if (response.ok) {
        msgElement.textContent = 'Message sent! A team member will reach out shortly.';
        msgElement.className = 'small text-success mt-1';
        form.reset();
        return;
      }

      const data = await response.json().catch(() => ({}));
      msgElement.textContent = data && data.errors && data.errors.length
        ? data.errors.map((error) => error.message).join(', ')
        : 'Could not send. Please call (561) 254-0241';
      msgElement.className = 'small text-danger mt-1';
    } catch (error) {
      msgElement.textContent = 'Could not send. Please call (561) 254-0241';
      msgElement.className = 'small text-danger mt-1';
    }
  }

  [
    ['signupForm', 'signupMsg'],
    ['contactForm', 'contactMsg']
  ].forEach(([formId, msgId]) => {
    const form = document.getElementById(formId);
    const msg = document.getElementById(msgId);
    if (!form || !msg) return;
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      await submitForm(form, msg);
    });
  });

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
      const field = document.querySelector('#contactForm textarea[name="message"], form[data-formspree-form] textarea[name="message"]');
      if (message && field) field.value = message;
    });
  });
})();
