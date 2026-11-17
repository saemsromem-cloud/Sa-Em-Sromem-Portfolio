// Contact form: friendly inline checks. The server repeats every check, so the form
// still works (and stays safe) without JavaScript.
(function () {
  "use strict";
  var form = document.querySelector("[data-contact-form]");
  if (!form) return;

  var rules = {
    name: function (v) { return v.length >= 2 ? "" : "Enter your name (at least 2 characters)."; },
    email: function (v) { return /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v) ? "" : "Enter a valid email address."; },
    subject: function (v) { return v.length >= 3 ? "" : "Enter a subject (at least 3 characters)."; },
    message: function (v) { return v.length >= 10 ? "" : "Write a message of at least 10 characters."; }
  };

  function show(field, text) {
    var id = field.id + "-error";
    var old = document.getElementById(id);
    if (old) old.remove();
    field.removeAttribute("aria-invalid");
    field.removeAttribute("aria-describedby");
    if (!text) return;
    var p = document.createElement("p");
    p.className = "field-error";
    p.id = id;
    p.textContent = text;
    field.setAttribute("aria-invalid", "true");
    field.setAttribute("aria-describedby", id);
    field.parentNode.insertBefore(p, field.nextSibling);
  }

  function check(field) {
    var text = rules[field.name](field.value.trim());
    show(field, text);
    return !text;
  }

  Object.keys(rules).forEach(function (name) {
    var field = form.elements[name];
    field.addEventListener("blur", function () { check(field); });
    field.addEventListener("input", function () { if (field.getAttribute("aria-invalid")) check(field); });
  });

  form.addEventListener("submit", function (event) {
    var firstBad = null;
    Object.keys(rules).forEach(function (name) {
      var field = form.elements[name];
      if (!check(field) && !firstBad) firstBad = field;
    });
    if (firstBad) { event.preventDefault(); firstBad.focus(); }
  });

  var message = form.elements.message;
  var counter = form.querySelector("[data-count]");
  if (message && counter) {
    var update = function () { counter.textContent = String(message.value.length); };
    message.addEventListener("input", update);
    update();
  }

  // After a send (or a rejected send) the status box sits at the top of the form: bring it into view.
  var status = document.getElementById("form-status");
  if (status && status.children.length) { status.scrollIntoView({ block: "center" }); status.focus(); }
})();
