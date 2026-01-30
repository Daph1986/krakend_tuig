(function () {
  // -----------------------------
  // CSRF helper (zoals jij had)
  // -----------------------------
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }

  const csrftoken = getCookie('csrftoken');

  const configEl = document.getElementById('planning-config');
  if (!configEl) return;

  const statusUrl = configEl.dataset.statusUrl;

  // -----------------------------
  // Helpers
  // -----------------------------
  function setCellStatusFromEl(el, status) {
    const cell = el.closest('.planning-cell');
    if (cell) cell.dataset.status = status || '';
  }

  function postStatus({ optredenId, status, userId }, onSuccess, onError) {
    const formData = new FormData();
    formData.append('optreden_id', optredenId);
    formData.append('status', status || '');
    if (userId) formData.append('user_id', userId);

    fetch(statusUrl, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      body: formData
    })
      .then(r => (r.ok ? r.json() : Promise.reject(r)))
      .then(() => onSuccess && onSuccess())
      .catch(() => onError && onError());
  }

  function closeAllDropdowns(except) {
    document.querySelectorAll('.planning-dropdown.is-open').forEach(dd => {
      if (except && dd === except) return;

      dd.classList.remove('is-open');
      dd.classList.remove('open-up');

      const btn = dd.querySelector('.planning-dd-btn');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  }

  // Betrouwbare heuristiek voor mobiel:
  // staat de knop in de onderste helft van het scherm? dan open-up.
  function setOpenDirection(dd, btn) {
    dd.classList.remove('open-up');

    const rect = btn.getBoundingClientRect();
    const viewportH = window.innerHeight;

    if (rect.top > viewportH * 0.5) {
      dd.classList.add('open-up');
    }
  }

  // -----------------------------
  // DESKTOP: native selects
  // -----------------------------
  const selects = document.querySelectorAll('.planning-select');

  // bij laden: zet de cel-status gelijk goed (voor kleuren)
  selects.forEach(sel => {
    setCellStatusFromEl(sel, sel.value || '');
  });

  selects.forEach(sel => {
    sel.addEventListener('change', () => {
      const optredenId = sel.dataset.optredenId;
      const status = sel.value; // '' of 'aanwezig' / 'afwezig' / 'onzeker'
      const userId = sel.dataset.userId || '';

      postStatus(
        { optredenId, status, userId },
        () => setCellStatusFromEl(sel, status),
        () => alert('Opslaan mislukt. Probeer opnieuw.')
      );
    });
  });

  // -----------------------------
  // MOBIEL: custom dropdown
  // -----------------------------
  const dropdowns = document.querySelectorAll('.planning-dropdown');

  // init: zet cell status + markeer selected
  dropdowns.forEach(dd => {
    const value = dd.dataset.value || '';
    setCellStatusFromEl(dd, value);

    dd.querySelectorAll('.planning-dd-item').forEach(item => {
      const v = item.dataset.value ?? '';
      if (v === value) item.classList.add('is-selected');
    });
  });

  // Event delegation (1 listener voor alles)
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.planning-dd-btn');
    const item = e.target.closest('.planning-dd-item');

    // Klik op dropdown button
    if (btn) {
      const dd = btn.closest('.planning-dropdown');
      if (!dd) return;

      if (btn.disabled || dd.dataset.disabled === '1') return;

      const isOpen = dd.classList.contains('is-open');

      // sluit andere dropdowns
      closeAllDropdowns(dd);

      if (!isOpen) {
        setOpenDirection(dd, btn);
        dd.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
      } else {
        dd.classList.remove('is-open');
        dd.classList.remove('open-up');
        btn.setAttribute('aria-expanded', 'false');
      }
      return;
    }

    // Klik op item (keuze)
    if (item) {
      const dd = item.closest('.planning-dropdown');
      if (!dd) return;

      const value = item.dataset.value ?? '';
      const labelText = item.textContent.trim();

      // UI update
      dd.dataset.value = value;

      const label = dd.querySelector('.planning-dd-label');
      if (label) label.textContent = labelText;

      dd.querySelectorAll('.planning-dd-item').forEach(i => i.classList.remove('is-selected'));
      item.classList.add('is-selected');

      // update celkleur direct
      setCellStatusFromEl(dd, value);

      // sluit menu
      dd.classList.remove('is-open');
      dd.classList.remove('open-up');

      const ddBtn = dd.querySelector('.planning-dd-btn');
      if (ddBtn) ddBtn.setAttribute('aria-expanded', 'false');

      // POST naar backend
      const optredenId = dd.dataset.optredenId;
      const userId = dd.dataset.userId || '';

      postStatus(
        { optredenId, status: value, userId },
        () => {},
        () => alert('Opslaan mislukt. Probeer opnieuw.')
      );

      return;
    }

    // Klik buiten: sluit alles
    closeAllDropdowns();
  });

  // Escape sluit dropdowns
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAllDropdowns();
  });

  // Scroll sluit dropdowns (voelt natuurlijk op mobiel)
  window.addEventListener('scroll', () => closeAllDropdowns(), { passive: true });
})();
