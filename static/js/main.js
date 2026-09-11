(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var navbar = document.querySelector('.navbar-ssa');
    if (navbar) {
      var toggleScrolled = function () {
        if (window.scrollY > 18) {
          navbar.classList.add('scrolled');
        } else {
          navbar.classList.remove('scrolled');
        }
      };
      toggleScrolled();
      window.addEventListener('scroll', toggleScrolled, { passive: true });
    }

    var forms = document.querySelectorAll('form[data-ssa-submit]');
    Array.prototype.forEach.call(forms, function (form) {
      form.addEventListener('submit', function () {
        var btn = form.querySelector('button[type="submit"]');
        if (btn) {
          btn.disabled = true;
          btn.setAttribute('data-original-text', btn.textContent);
          btn.innerHTML =
            '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>' +
            (btn.getAttribute('data-loading-text') || 'Please wait...');
        }
      });
    });

    if (typeof htmx !== 'undefined') {
      htmx.config.useTemplateFragments = true;
      htmx.config.defaultSwapStyle = 'innerHTML';
      document.body.addEventListener('htmx:beforeSwap', function (evt) {
        if (evt.detail.xhr && evt.detail.xhr.status >= 400) {
          evt.detail.shouldSwap = true;
          evt.detail.isError = true;
        }
      });
    }

    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var href = a.getAttribute('href');
        if (href.length > 1) {
          var target = document.querySelector(href);
          if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      });
    });
  });
})();
