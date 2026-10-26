"""HTML du formulaire de contact partagé par les générateurs.

L'identifiant GoHighLevel est dans src/assets/cdf-contact.js
(constante CDF_GHL_FORM_ID). Si l'iframe ou form_embed.js ne charge pas,
le bloc garde le formulaire courriel vers l'adresse déjà publiée.
"""

EMAIL = "p-o.chiasson@remax-quebec.com"
STYLESHEET = '<link rel="stylesheet" href="/src/assets/cdf-contact.css">'
SCRIPT = '<script src="/src/assets/cdf-contact.js" defer></script>'

MOUNT = """<div class="cdf-contact" data-cdf-contact>
<h3 class="cdf-contact-title" id="cdf-contact-title">Écrire à l'équipe</h3>
<p class="cdf-contact-lead">Écrivez à l'équipe. Le message s'ouvre dans votre logiciel de courriel, prêt à envoyer.</p>
<p class="cdf-contact-note">Les champs marqués d'un astérisque sont obligatoires.</p>
<form class="cdf-contact-form" action="mailto:p-o.chiasson@remax-quebec.com?subject=Message%20du%20site%20chiassondefrancesco.ca" method="post" enctype="text/plain">
<input name="page" type="hidden" value="">
<label for="cdf-nom">Nom <span class="cdf-contact-req" aria-hidden="true">*</span>
<input id="cdf-nom" name="nom" type="text" autocomplete="name" required maxlength="120">
</label>
<label for="cdf-courriel">Courriel <span class="cdf-contact-req" aria-hidden="true">*</span>
<input id="cdf-courriel" name="courriel" type="email" autocomplete="email" inputmode="email" required maxlength="160">
</label>
<label class="cdf-contact-span" for="cdf-telephone">Téléphone
<input id="cdf-telephone" name="telephone" type="tel" autocomplete="tel" inputmode="tel" maxlength="40">
</label>
<label class="cdf-contact-span" for="cdf-message">Message <span class="cdf-contact-req" aria-hidden="true">*</span>
<textarea id="cdf-message" name="message" required maxlength="2000" rows="5"></textarea>
</label>
<div class="cdf-contact-span cdf-contact-consent">
<input id="cdf-consent" name="consentement" type="checkbox" value="oui" required>
<span><label for="cdf-consent">J'accepte que l'équipe Chiasson De Francesco utilise ces renseignements pour répondre à ma demande.</label> <a href="/confidentialite.html">Politique de confidentialité</a>.</span>
</div>
<div class="cdf-contact-span">
<button class="cdf-contact-submit" type="submit">Envoyer le message</button>
</div>
</form>
<div class="cdf-contact-direct">
<p>Ou joignez l'équipe directement.</p>
<p><a href="mailto:p-o.chiasson@remax-quebec.com">p-o.chiasson@remax-quebec.com</a></p>
<p><a href="tel:+18199194631">819-919-4631</a></p>
</div>
</div>"""
