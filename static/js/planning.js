(function () {
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
  const selects = document.querySelectorAll('.planning-select');

  // ✅ bij laden: zet de cel-status gelijk goed (voor kleuren)
  selects.forEach(sel => {
    const td = sel.closest('.planning-cell');
    if (td) td.dataset.status = sel.value || '';
  });

  function postStatus(selectEl) {
    const optredenId = selectEl.dataset.optredenId;
    const status = selectEl.value; // '' of 'aanwezig' / 'afwezig' / 'onzeker'
    const userId = selectEl.dataset.userId || '';

    const formData = new FormData();
    formData.append('optreden_id', optredenId);
    formData.append('status', status);
    if (userId) formData.append('user_id', userId);

    fetch(statusUrl, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      body: formData
    })
      .then(r => r.ok ? r.json() : Promise.reject(r))
      .then(() => {
        // ✅ na opslaan: update celkleur direct
        const td = selectEl.closest('.planning-cell');
        if (td) td.dataset.status = status || '';
      })
      .catch(() => {
        alert('Opslaan mislukt. Probeer opnieuw.');
      });
  }

  selects.forEach(sel => {
    sel.addEventListener('change', () => postStatus(sel));
  });
})();
