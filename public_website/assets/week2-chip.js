(function () {
  const W = window.CIRCA_WEEK2;
  if (!W) return;
  const N_ALIVE = W.nAlive;
  const POT = W.pot;
  const SAVE_KEY = W.saveKey;
  const CROWD = W.share;
  const IMPLIED = W.implied;
  const GAMES = W.games;
  const ESPN_LOGO = { JAC: "jax", WAS: "wsh" };

  const NAMES = {
    ARI: "Cardinals", ATL: "Falcons", BAL: "Ravens", BUF: "Bills",
    CAR: "Panthers", CHI: "Bears", CIN: "Bengals", CLE: "Browns",
    DAL: "Cowboys", DEN: "Broncos", DET: "Lions", GB: "Packers",
    HOU: "Texans", IND: "Colts", JAC: "Jaguars", KC: "Chiefs",
    LAC: "Chargers", LAR: "Rams", LV: "Raiders", MIA: "Dolphins",
    MIN: "Vikings", NE: "Patriots", NO: "Saints", NYG: "Giants",
    NYJ: "Jets", PHI: "Eagles", PIT: "Steelers", SEA: "Seahawks",
    SF: "49ers", TB: "Buccaneers", TEN: "Titans", WAS: "Commanders"
  };

  const BOOK = [
    { id: "jac", n: 4, burned: "JAC", label: "JAC×4" },
    { id: "pit", n: 2, burned: "PIT", label: "PIT×2" },
    { id: "lv", n: 2, burned: "LV", label: "LV×2" }
  ];

  const TEAMS = Object.keys(NAMES).sort(function (a, b) {
    return (CROWD[b] || 0) - (CROWD[a] || 0);
  });

  const state = { win: {}, pick: { jac: "", pit: "", lv: "" } };

  function favorite(g) {
    return IMPLIED[g.home] >= IMPLIED[g.away] ? g.home : g.away;
  }

  function logoUrl(abbr) {
    return "https://a.espncdn.com/i/teamlogos/nfl/500/" + (ESPN_LOGO[abbr] || abbr).toLowerCase() + ".png";
  }

  function pct(team) {
    return 100 * (CROWD[team] || 0);
  }

  function money(n) {
    return "$" + Math.round(n).toLocaleString("en-US");
  }

  function resetFavorites() {
    GAMES.forEach(function (g) { state.win[g.id] = favorite(g); });
  }

  function load() {
    resetFavorites();
    try {
      var raw = localStorage.getItem(SAVE_KEY);
      if (!raw) return;
      var s = JSON.parse(raw);
      GAMES.forEach(function (g) {
        if (s.win && (s.win[g.id] === g.away || s.win[g.id] === g.home)) state.win[g.id] = s.win[g.id];
      });
      BOOK.forEach(function (b) {
        var t = s.pick && s.pick[b.id];
        if (t && NAMES[t] && t !== b.burned) state.pick[b.id] = t;
      });
    } catch (e) {}
  }

  function save() {
    localStorage.setItem(SAVE_KEY, JSON.stringify({ win: state.win, pick: state.pick }));
  }

  function snapshot() {
    var winners = {};
    var share = 0;
    GAMES.forEach(function (g) {
      var t = state.win[g.id] || favorite(g);
      winners[t] = true;
      share += CROWD[t] || 0;
    });
    var fieldAlive = N_ALIVE * share;
    var chip = POT / Math.max(fieldAlive, 1);
    var oursLive = 0;
    var oursDead = 0;
    var portfolio = 0;
    var rows = BOOK.map(function (b) {
      var team = state.pick[b.id] || "";
      var live = Boolean(team && winners[team]);
      if (team) {
        if (live) {
          oursLive += b.n;
          portfolio += b.n * chip;
        } else {
          oursDead += b.n;
        }
      }
      return { book: b, team: team, live: live, ev: team && live ? chip : 0 };
    });
    var chalkDown = ["SF", "TB", "BAL", "LAC"].filter(function (t) { return !winners[t]; });
    return {
      winners: winners,
      share: share,
      fieldAlive: fieldAlive,
      fieldDead: N_ALIVE - fieldAlive,
      chip: chip,
      rows: rows,
      oursLive: oursLive,
      oursDead: oursDead,
      unset: 8 - oursLive - oursDead,
      portfolio: portfolio,
      chalkDown: chalkDown
    };
  }

  function optionList(burned, selected) {
    var html = '<option value="">— pick —</option>';
    TEAMS.forEach(function (t) {
      if (t === burned) return;
      html += '<option value="' + t + '"' + (t === selected ? " selected" : "") + ">"
        + t + " · " + pct(t).toFixed(1) + "%</option>";
    });
    return html;
  }

  function sideHtml(g, team, win) {
    var isWin = team === win;
    var isFav = team === favorite(g);
    var cls = "chip-side" + (isWin ? " win" : "") + (isFav ? " fav" : "");
    return '<button type="button" class="' + cls + '" data-chip-game="' + g.id + '" data-chip-team="' + team + '">'
      + '<img src="' + logoUrl(team) + '" alt="" width="28" height="28" onerror="this.remove()" />'
      + "<strong>" + team + "</strong>"
      + '<span class="chip-meta">' + NAMES[team] + " · crowd " + pct(team).toFixed(1)
      + "% · " + (100 * IMPLIED[team]).toFixed(0) + "% win</span>"
      + '<span class="badge">' + (isWin ? "WIN" : isFav ? "FAV" : "DOG") + "</span>"
      + "</button>";
  }

  function render() {
    var root = document.getElementById("week2Chip");
    if (!root) return;
    var snap = snapshot();
    var read = snap.chalkDown.length
      ? "Chalk down: " + snap.chalkDown.join(", ") + " — field shrinks, live tickets get a bigger chip."
      : "Favorites hold. Almost the whole 16,978 field survives, so a live ticket sits near the $1,000 fee.";

    root.querySelector("#chipRead").textContent = read;
    document.getElementById("chipStrip").innerHTML =
      '<div class="stat"><span>Field alive</span><b>' + snap.fieldAlive.toLocaleString("en-US", { maximumFractionDigits: 0 }) + "</b></div>"
      + '<div class="stat"><span>Field dead</span><b class="neg">' + snap.fieldDead.toLocaleString("en-US", { maximumFractionDigits: 0 }) + "</b></div>"
      + '<div class="stat"><span>Chip / live entry</span><b class="pos">' + money(snap.chip) + "</b></div>"
      + '<div class="stat"><span>Our live / dead / unset</span><b>' + snap.oursLive + " / " + snap.oursDead + " / " + snap.unset + "</b></div>"
      + '<div class="stat"><span>Our 8 tickets</span><b class="pos">' + money(snap.portfolio) + "</b></div>";

    document.getElementById("chipBook").innerHTML = snap.rows.map(function (r) {
      var status = !r.team ? "unset" : r.live ? "live" : "dead";
      var cls = !r.team ? "" : r.live ? "pos" : "neg";
      return '<div class="chip-ticket">'
        + "<div><b>" + r.book.label + "</b><span>burned " + r.book.burned + "</span></div>"
        + '<select data-chip-pick="' + r.book.id + '">' + optionList(r.book.burned, r.team) + "</select>"
        + '<span class="' + cls + '">' + status + " · " + (r.team ? money(r.ev) + " × " + r.book.n : "—") + "</span>"
        + "</div>";
    }).join("");

    document.getElementById("chipBoard").innerHTML = GAMES.map(function (g) {
      var win = state.win[g.id] || favorite(g);
      return '<div class="chip-game">'
        + '<div class="when">' + g.when + " · " + g.away + " @ " + g.home + " · " + g.line + "</div>"
        + '<div class="chip-sides">' + sideHtml(g, g.away, win) + sideHtml(g, g.home, win) + "</div>"
        + "</div>";
    }).join("");
    save();
  }

  function init() {
    var root = document.getElementById("week2Chip");
    if (!root) return;
    load();
    root.addEventListener("click", function (e) {
      if (e.target.id === "chipFavs") {
        resetFavorites();
        render();
        return;
      }
      var btn = e.target.closest("[data-chip-game]");
      if (!btn) return;
      state.win[btn.getAttribute("data-chip-game")] = btn.getAttribute("data-chip-team");
      render();
    });
    root.addEventListener("change", function (e) {
      var id = e.target.getAttribute("data-chip-pick");
      if (!id) return;
      state.pick[id] = e.target.value || "";
      render();
    });
    render();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
