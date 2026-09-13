'use strict';
document.documentElement.classList.add('js-ready');
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
document.querySelectorAll('.submenu-toggle').forEach(button => {
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    document.querySelectorAll('.nav-group.open').forEach(group => {
      group.classList.remove('open');
      group.querySelector('button').setAttribute('aria-expanded', 'false');
    });
    button.setAttribute('aria-expanded', String(open));
    button.closest('.nav-group').classList.toggle('open', open);
  });
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const active = document.querySelector('.nav-group.open');
  if (active) {
    active.classList.remove('open');
    const button = active.querySelector('button');
    button.setAttribute('aria-expanded', 'false');
    button.focus();
  } else if (navigation.classList.contains('is-open')) {
    navigation.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
    menu.focus();
  }
});
document.addEventListener('click', event => {
  document.querySelectorAll('.nav-group.open').forEach(group => {
    if (!group.contains(event.target)) {
      group.classList.remove('open');
      group.querySelector('button').setAttribute('aria-expanded', 'false');
    }
  });
});
document.querySelectorAll('.result-form').forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const text = ['Name: ' + data.get('name'), 'School: ' + data.get('school'), 'Competition: ' + data.get('competition'), 'Fixture date: ' + data.get('date'), 'Teams and final score: ' + data.get('score')].join('\r\n');
    const link = 'mailto:info@hsaa.org.uk?subject=' + encodeURIComponent('HSAA result: ' + data.get('competition')) + '&body=' + encodeURIComponent(text);
    window.location.href = link;
    form.querySelector('.form-status').textContent = 'Your result is ready in your email app. Please review and send it. If your email app did not open, email these details to info@hsaa.org.uk. This website has not sent or stored your result.';
  });
});
