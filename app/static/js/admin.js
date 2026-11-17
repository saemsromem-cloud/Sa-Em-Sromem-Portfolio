// Admin dashboard: search, message dialog, delete confirmation.
(function () {
  "use strict";

  var table = document.getElementById("message-table");
  var search = document.getElementById("message-search");
  var empty = document.getElementById("no-results");

  if (table && search) {
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    search.addEventListener("input", function () {
      var term = search.value.toLowerCase().trim();
      var shown = 0;
      rows.forEach(function (row) {
        var match = row.textContent.toLowerCase().indexOf(term) !== -1;
        row.hidden = !match;
        if (match) shown += 1;
      });
      if (empty) empty.hidden = shown !== 0;
    });
  }

  var dialog = document.getElementById("message-dialog");
  document.querySelectorAll(".view-message").forEach(function (button) {
    button.addEventListener("click", function () {
      document.getElementById("dialog-subject").textContent = button.dataset.subject;
      document.getElementById("dialog-meta").textContent =
        button.dataset.name + " <" + button.dataset.email + "> on " + button.dataset.date;
      document.getElementById("dialog-message").textContent = button.dataset.message;
      if (dialog && dialog.showModal) dialog.showModal();
    });
  });

  document.querySelectorAll(".confirm-delete").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!window.confirm("Delete this message? This cannot be undone.")) event.preventDefault();
    });
  });
})();
