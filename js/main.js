'use strict';
document.documentElement.classList.add('js-ready');
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation.classList.contains('is-open')) {
    navigation.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
    menu.focus();
  }
});
document.querySelectorAll('.result-form').forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const text = ['Name: ' + data.get('name'), (form.dataset.organisation || 'School') + ': ' + data.get('school'), 'Competition: ' + data.get('competition'), 'Fixture date: ' + data.get('date'), 'Teams and final score: ' + data.get('score')].join('\r\n');
    const link = 'mailto:info@hsaa.org.uk?subject=' + encodeURIComponent('HSAA result: ' + data.get('competition')) + '&body=' + encodeURIComponent(text);
    window.location.href = link;
    form.querySelector('.form-status').textContent = 'Your result is ready in your email app. Please review and send it. If your email app did not open, email these details to info@hsaa.org.uk. This website has not sent or stored your result.';
  });
});

const ticker = document.querySelector('.news-ticker');
if (ticker) {
  const track = ticker.querySelector('.ticker-track');
  const copy = ticker.querySelector('.ticker-items').cloneNode(true);
  copy.setAttribute('aria-hidden', 'true');
  track.appendChild(copy);
  ticker.classList.add('is-animated');

}

// Close sibling disclosures and support dismissal without losing keyboard focus.
navigation.querySelectorAll('details').forEach(group => {
  group.addEventListener('toggle', () => {
    if (!group.open) return;
    const list = group.parentElement.parentElement;
    Array.from(list.children).forEach(item => {
      const sibling = item.querySelector(':scope > details');
      if (sibling && sibling !== group) sibling.open = false;
    });
  });
});
document.addEventListener('click', event => {
  if (!navigation.contains(event.target) && !menu.contains(event.target)) {
    navigation.querySelectorAll('details[open]').forEach(group => { group.open = false; });
    navigation.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
  }
});
navigation.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const group = event.target.closest('details[open]');
  if (group) {
    event.stopPropagation();
    group.open = false;
    group.querySelector('summary').focus();
  }
});

document.querySelectorAll('.membership-form').forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const fields = [
      ['Full name', 'name'], ['Email', 'email'], ['Mobile number', 'mobile'],
      ['Season represented', 'season'], ['District manager', 'manager'],
      ['Membership category', 'category'], ['First teammate', 'teammate1'],
      ['Second teammate', 'teammate2'], ['Can teammates be contacted', 'contact-teammates'],
      ['Teammates email addresses', 'teammate-emails'], ['Support annual event', 'annual-event']
    ];
    const body = fields.map(([label, key]) => label + ': ' + (data.get(key) || 'Not provided')).join('\r\n');
    window.location.href = 'mailto:info@hsaa.org.uk?subject=' + encodeURIComponent('HSAA Alumni Network membership') + '&body=' + encodeURIComponent(body);
    form.querySelector('.form-status').textContent = 'Please review and send your membership enquiry in your email app. If it did not open, email your details to info@hsaa.org.uk. This website has not sent or stored your details.';
  });
});
