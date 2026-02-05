// static/js/profile_photo_preview.js
(() => {
  const input = document.querySelector('[data-photo-input]');
  const preview = document.querySelector('[data-photo-preview]');

  if (!input || !preview) return;

  let previousObjectUrl = null;

  input.addEventListener('change', () => {
    const file = input.files && input.files[0];
    if (!file) return;

    // alleen images
    if (!file.type || !file.type.startsWith('image/')) return;

    // oude blob-url opruimen
    if (previousObjectUrl) {
      URL.revokeObjectURL(previousObjectUrl);
    }

    const objectUrl = URL.createObjectURL(file);
    previousObjectUrl = objectUrl;

    preview.src = objectUrl;
    preview.classList.remove('d-none');
  });

  // extra: opruimen bij verlaten pagina
  window.addEventListener('beforeunload', () => {
    if (previousObjectUrl) URL.revokeObjectURL(previousObjectUrl);
  });
})();
