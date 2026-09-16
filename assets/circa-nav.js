(function () {
  function weekFromUrl() {
    var q = new URLSearchParams(location.search).get("week");
    if (q === "1" || q === "2") return q;
    return document.body.getAttribute("data-default-week") || "1";
  }

  function setWeek(week, push) {
    document.body.setAttribute("data-week", week);
    document.querySelectorAll("[data-set-week]").forEach(function (btn) {
      btn.classList.toggle("on", btn.getAttribute("data-set-week") === week);
    });
    var label = document.querySelector("[data-week-label]");
    if (label) {
      var custom = label.getAttribute("data-label-" + week);
      label.textContent = custom || ("Week " + week);
    }
    document.querySelectorAll("a[data-carry-week]").forEach(function (a) {
      var raw = a.getAttribute("data-href") || a.getAttribute("href");
      var parts = raw.split("#");
      var path = parts[0].split("?")[0];
      var hash = parts[1] ? "#" + parts[1] : "";
      a.setAttribute("href", path + "?week=" + week + hash);
    });
    var url = new URL(location.href);
    url.searchParams.set("week", week);
    if (push) history.pushState({ week: week }, "", url);
    else history.replaceState({ week: week }, "", url);
    var hooks = window.CircaNavHooks || [];
    hooks.forEach(function (fn) {
      try { fn(week); } catch (e) {}
    });
  }

  function init() {
    setWeek(weekFromUrl(), false);
    document.querySelectorAll("[data-set-week]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        setWeek(btn.getAttribute("data-set-week"), true);
      });
    });
    window.addEventListener("popstate", function () {
      setWeek(weekFromUrl(), false);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
