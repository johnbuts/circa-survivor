(function () {
  var PAGES = { "1": "week1.html", "2": "week2.html", "3": "week3.html", "4": "week4.html", "5": "week5.html" };
  var HEDGE_WEEKS = ["1", "2", "3", "5"];

  function toRoot(path) {
    var root = document.body.getAttribute("data-root") || "";
    if (!root) return path;
    var up = root.split("/").filter(Boolean).map(function () { return ".."; }).join("/");
    return (up ? up + "/" : "") + path;
  }

  function weekFromPage() {
    var page = document.body.getAttribute("data-page");
    var q = new URLSearchParams(location.search).get("week");
    if (page === "hedge" && HEDGE_WEEKS.indexOf(q) >= 0) return q;
    return document.body.getAttribute("data-week") || "5";
  }

  function init() {
    var week = weekFromPage();
    document.body.setAttribute("data-week", week);

    var page = document.body.getAttribute("data-page");
    var markWeek = page === "hub" || page === "hedge" || page === "field";
    document.querySelectorAll("[data-week-link]").forEach(function (a) {
      var n = a.getAttribute("data-week-link");
      if (page === "hedge" && HEDGE_WEEKS.indexOf(n) >= 0) {
        a.setAttribute("href", "?week=" + n);
      } else {
        a.setAttribute("href", toRoot(PAGES[n]));
      }
      a.classList.toggle("on", markWeek && n === week);
    });

    document.querySelectorAll("[data-hub]").forEach(function (a) {
      a.setAttribute("href", toRoot(PAGES[week]));
    });

    document.querySelectorAll("[data-hedge]").forEach(function (a) {
      var hw = HEDGE_WEEKS.indexOf(week) >= 0 ? week : "5";
      a.setAttribute("href", toRoot("pick_selection/week1/index.html?week=" + hw));
    });

    var label = document.querySelector("[data-week-label]");
    if (label) {
      var custom = label.getAttribute("data-label-" + week);
      if (custom) label.textContent = custom;
    }

    var hooks = window.CircaNavHooks || [];
    hooks.forEach(function (fn) {
      try { fn(week); } catch (e) {}
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
