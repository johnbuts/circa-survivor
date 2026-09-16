(function () {
  function files() {
    return window.CIRCA_FILES || {};
  }

  function repoPathFromHref(href) {
    var root = document.body.getAttribute("data-root") || "";
    var cleaned = String(href || "").split("#")[0].split("?")[0];
    if (!cleaned) return "";
    try {
      var u = new URL(cleaned, "https://circa.local/" + root);
      return decodeURIComponent(u.pathname.replace(/^\//, ""));
    } catch (e) {
      return cleaned.replace(/^\.\//, "");
    }
  }

  function isDocPath(path) {
    return /\.(md|csv)$/i.test(path || "");
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function inlineFmt(raw) {
    var s = escapeHtml(raw);
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, function (_, label, url) {
      var path = repoPathFromHref(url);
      if (isDocPath(path) && files()[path]) {
        return '<a href="view.html?f=' + encodeURIComponent(path) + '" data-open-doc="' + escapeHtml(path) + '">' + label + "</a>";
      }
      if (/^(https?:|mailto:)/i.test(url)) {
        return '<a href="' + escapeHtml(url) + '" target="_blank" rel="noopener">' + label + "</a>";
      }
      var href = url;
      var root = document.body.getAttribute("data-root") || "";
      if (root && !/^[./]/.test(url) && url.indexOf(":") < 0) {
        var ups = root.split("/").filter(Boolean).map(function () { return ".."; }).join("/");
        href = (ups ? ups + "/" : "") + url;
      }
      return '<a href="' + escapeHtml(href) + '">' + label + "</a>";
    });
    return s;
  }

  function renderCsv(text) {
    var rows = String(text).replace(/\r/g, "").split("\n").filter(function (ln, i, arr) {
      return ln.length || i < arr.length - 1;
    });
    if (!rows.length) return "<p class=\"hint\">Empty file.</p>";
    function split(line) {
      var out = [];
      var cur = "";
      var q = false;
      for (var i = 0; i < line.length; i++) {
        var c = line[i];
        if (c === '"') {
          q = !q;
        } else if (c === "," && !q) {
          out.push(cur);
          cur = "";
        } else {
          cur += c;
        }
      }
      out.push(cur);
      return out;
    }
    var html = "<div class=\"wrap\"><table class=\"doc-table\">";
    rows.forEach(function (line, i) {
      if (!line && i === rows.length - 1) return;
      var cells = split(line);
      var tag = i === 0 ? "th" : "td";
      html += "<tr>" + cells.map(function (cell) {
        return "<" + tag + ">" + escapeHtml(cell) + "</" + tag + ">";
      }).join("") + "</tr>";
    });
    html += "</table></div>";
    return html;
  }

  function renderMd(text) {
    var lines = String(text).replace(/\r/g, "").split("\n");
    var html = [];
    var i = 0;
    function flushList(items, ordered) {
      if (!items.length) return;
      html.push(ordered ? "<ol>" : "<ul>");
      items.forEach(function (it) { html.push("<li>" + inlineFmt(it) + "</li>"); });
      html.push(ordered ? "</ol>" : "</ul>");
      items.length = 0;
    }
    var ul = [];
    var ol = [];
    while (i < lines.length) {
      var line = lines[i];
      if (/^\s*$/.test(line)) {
        flushList(ul, false);
        flushList(ol, true);
        i += 1;
        continue;
      }
      if (/^\s*\|/.test(line) && i + 1 < lines.length && /^\s*\|?\s*:?-/.test(lines[i + 1])) {
        flushList(ul, false);
        flushList(ol, true);
        var table = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) {
          table.push(lines[i]);
          i += 1;
        }
        html.push("<div class=\"wrap\"><table class=\"doc-table\">");
        table.forEach(function (row, ri) {
          if (ri === 1 && /:?-+:?/.test(row)) return;
          var cells = row.replace(/^\s*\|/, "").replace(/\|\s*$/, "").split("|");
          var tag = ri === 0 ? "th" : "td";
          html.push("<tr>" + cells.map(function (cell) {
            return "<" + tag + ">" + inlineFmt(cell.trim()) + "</" + tag + ">";
          }).join("") + "</tr>");
        });
        html.push("</table></div>");
        continue;
      }
      var h = line.match(/^(#{1,3})\s+(.*)$/);
      if (h) {
        flushList(ul, false);
        flushList(ol, true);
        html.push("<h" + h[1].length + ">" + inlineFmt(h[2]) + "</h" + h[1].length + ">");
        i += 1;
        continue;
      }
      if (/^---+$/.test(line.trim())) {
        flushList(ul, false);
        flushList(ol, true);
        html.push("<hr />");
        i += 1;
        continue;
      }
      var uli = line.match(/^\s*[-*]\s+(.*)$/);
      if (uli) {
        flushList(ol, true);
        ul.push(uli[1]);
        i += 1;
        continue;
      }
      var oli = line.match(/^\s*\d+\.\s+(.*)$/);
      if (oli) {
        flushList(ul, false);
        ol.push(oli[1]);
        i += 1;
        continue;
      }
      flushList(ul, false);
      flushList(ol, true);
      html.push("<p>" + inlineFmt(line) + "</p>");
      i += 1;
    }
    flushList(ul, false);
    flushList(ol, true);
    return html.join("");
  }

  function renderFile(path) {
    var body = files()[path];
    if (body == null) {
      return '<p class="hint">Not bundled in the site. Path: <span class="mono">' + escapeHtml(path) + "</span></p>";
    }
    if (/\.csv$/i.test(path)) return renderCsv(body);
    return '<div class="md">' + renderMd(body) + "</div>";
  }

  function ensureOverlay() {
    var el = document.getElementById("circa-viewer");
    if (el) return el;
    el = document.createElement("div");
    el.id = "circa-viewer";
    el.hidden = true;
    el.innerHTML =
      '<div class="cv-scrim" data-cv-close="1"></div>' +
      '<div class="cv-panel" role="dialog" aria-modal="true">' +
      '<div class="cv-bar"><span class="mono" id="cv-title"></span>' +
      '<button type="button" class="ghost" data-cv-close="1">Close</button></div>' +
      '<div class="cv-body" id="cv-body"></div></div>';
    document.body.appendChild(el);
    el.addEventListener("click", function (e) {
      if (e.target.getAttribute("data-cv-close")) closeViewer();
      var open = e.target.closest("[data-open-doc]");
      if (open) {
        e.preventDefault();
        showPath(open.getAttribute("data-open-doc"));
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeViewer();
    });
    return el;
  }

  function showPath(path) {
    if (!path) return;
    var overlay = ensureOverlay();
    overlay.hidden = false;
    document.getElementById("cv-title").textContent = path;
    document.getElementById("cv-body").innerHTML = renderFile(path);
    overlay.querySelector(".cv-body").scrollTop = 0;
  }

  function closeViewer() {
    var el = document.getElementById("circa-viewer");
    if (el) el.hidden = true;
  }

  function init() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]");
      if (!a) return;
      if (a.hasAttribute("data-open-doc")) {
        e.preventDefault();
        showPath(a.getAttribute("data-open-doc"));
        return;
      }
      var href = a.getAttribute("href") || "";
      if (/^(https?:|mailto:|#)/i.test(href)) return;
      var path = repoPathFromHref(href);
      if (!isDocPath(path)) return;
      e.preventDefault();
      showPath(path);
    });
  }

  window.CircaView = {
    show: showPath,
    renderFile: renderFile,
    repoPathFromHref: repoPathFromHref,
    files: files
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
