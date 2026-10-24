(function () {
  var form = document.getElementById('intake');
  if (!form) return;
  var email = (window.AGENCY_EMAIL || '').trim();
  var note = document.getElementById('mode-note');
  note.textContent = email
    ? "En cliquant sur Envoyer, votre messagerie s'ouvre avec votre demande déjà écrite. Il vous reste à l'envoyer."
    : "Votre demande est préparée ici, puis vous l'envoyez en message Instagram. Rien n'est envoyé sans vous.";

  var params = new URLSearchParams(location.search);
  var f = params.get('formule');
  if (f && form.formule.querySelector('option[value="' + f + '"]')) form.formule.value = f;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var err = document.getElementById('form-error');
    var missing = [];
    form.querySelectorAll('[required]').forEach(function (el) {
      var ok = el.type === 'checkbox' ? el.checked : el.value.trim() !== '';
      if (ok && el.type === 'email') ok = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value.trim());
      el.setAttribute('aria-invalid', ok ? 'false' : 'true');
      if (!ok) missing.push(el.labels && el.labels[0] ? el.labels[0].textContent.trim() : el.name);
    });
    if (missing.length) {
      err.hidden = false;
      err.textContent = 'À compléter : ' + missing.join(', ');
      return;
    }
    err.hidden = true;
    var lines = [
      'Demande de page, tonsite.beaute',
      'Formule : ' + form.formule.options[form.formule.selectedIndex].text,
      'Métier : ' + form.metier.value,
      'Nom : ' + form.nom.value,
      'Activité : ' + form.commerce.value,
      'Ville : ' + form.ville.value,
      'Instagram ou TikTok : ' + (form.insta.value || 'non donné'),
      'Réservation actuelle : ' + form.outil.value,
      'Lien de réservation : ' + (form.lien.value || 'non donné'),
      'E-mail : ' + form.email.value,
      'Téléphone : ' + (form.tel.value || 'non donné'),
      'Message : ' + (form.message.value || ''),
      'Notice de confidentialité lue : oui'
    ];
    var text = lines.join('\n');
    if (email) {
      location.href = 'mailto:' + email + '?subject=' + encodeURIComponent('Demande de page, ' + form.commerce.value) + '&body=' + encodeURIComponent(text);
      return;
    }
    form.hidden = true;
    var res = document.getElementById('result');
    res.hidden = false;
    document.getElementById('result-text').textContent = "Copiez votre demande, puis collez-la dans un message Instagram à @tonsite.beaute. On vous répond par message.";
    var s = document.getElementById('summary');
    s.value = text;
    document.getElementById('copy').addEventListener('click', function () {
      s.select();
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(
        function () { document.getElementById('copy').textContent = 'Copié'; },
        function () { document.execCommand('copy'); document.getElementById('copy').textContent = 'Copié'; }
      );
    });
  });
})();
