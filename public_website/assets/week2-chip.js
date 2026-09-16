(function () {
  const N_ALIVE = 16978;
  const POT = 25017000;
  const SAVE_KEY = "circa-week2-chip-v2";
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

  const CROWD = {
    ARI: 1.3943705648868252e-6, ATL: 1.2753632683457028e-5,
    BAL: 0.10645796043828966, BUF: 0.008550550342272284,
    CAR: 0.009204876645686613, CHI: 0.024427728567870125,
    CIN: 5.970648391037287e-6, CLE: 5.697772054577946e-9,
    DAL: 0.00785933199272295, DEN: 0.0017540803744997696,
    DET: 2.740263566237214e-7, GB: 0.008832778331956727,
    HOU: 0.004199172219601526, IND: 2.0115350196653298e-8,
    JAC: 7.501640434244362e-6, KC: 0.034913122742187365,
    LAC: 0.09125240026822662, LAR: 0.03586144254614909,
    LV: 3.5112932509550235e-8, MIA: 2.7180354421884392e-11,
    MIN: 5.2470658944795595e-8, NE: 0.01874905935504819,
    NO: 1.2649210095812257e-9, NYG: 9.576945412208352e-9,
    NYJ: 4.871434591302524e-7, PHI: 0.04524369827702494,
    PIT: 8.949057994581865e-8, SEA: 0.005566504573264036,
    SF: 0.3047006607045309, TB: 0.2923974878736724,
    TEN: 1.0709439484022541e-8, WAS: 5.388193568040223e-7
  };

  const IMPLIED = {
    ARI: 0.34266768426650496, ATL: 0.4104985551235768,
    BAL: 0.773901907872687, BUF: 0.657332315733495,
    CAR: 0.5895014448764232, CHI: 0.6891589978565722,
    CIN: 0.4104985551235768, CLE: 0.226098092127313,
    DAL: 0.657332315733495, DEN: 0.5895014448764232,
    DET: 0.34266768426650496, GB: 0.657332315733495,
    HOU: 0.5895014448764232, IND: 0.28070800621787956,
    JAC: 0.4104985551235768, KC: 0.7192919937821205,
    LAC: 0.7336719810356634, LAR: 0.7336719810356634,
    LV: 0.26632801896433655, MIA: 0.12408679611587599,
    MIN: 0.3108410021434278, NE: 0.6891589978565722,
    NO: 0.226098092127313, NYG: 0.26632801896433655,
    NYJ: 0.34266768426650496, PHI: 0.7336719810356634,
    PIT: 0.3108410021434278, SEA: 0.657332315733495,
    SF: 0.875913203884124, TB: 0.773901907872687,
    TEN: 0.26632801896433655, WAS: 0.34266768426650496
  };

  const GAMES = [
    { id: "det-buf", when: "Thu 8:15 ET", away: "DET", home: "BUF", line: "BUF −4.5" },
    { id: "car-atl", when: "Sun 1:00 ET", away: "CAR", home: "ATL", line: "CAR −2.5" },
    { id: "no-bal", when: "Sun 1:00 ET", away: "NO", home: "BAL", line: "BAL −8.5" },
    { id: "min-chi", when: "Sun 1:00 ET", away: "MIN", home: "CHI", line: "CHI −5.5" },
    { id: "cin-hou", when: "Sun 1:00 ET", away: "CIN", home: "HOU", line: "HOU −2.5" },
    { id: "cle-tb", when: "Sun 1:00 ET", away: "CLE", home: "TB", line: "TB −8.5" },
    { id: "gb-nyj", when: "Sun 1:00 ET", away: "GB", home: "NYJ", line: "GB −4.5" },
    { id: "pit-ne", when: "Sun 1:00 ET", away: "PIT", home: "NE", line: "NE −5.5" },
    { id: "phi-ten", when: "Sun 1:00 ET", away: "PHI", home: "TEN", line: "PHI −7" },
    { id: "jac-den", when: "Sun 4:05 ET", away: "JAC", home: "DEN", line: "DEN −2.5" },
    { id: "lv-lac", when: "Sun 4:05 ET", away: "LV", home: "LAC", line: "LAC −7" },
    { id: "sea-ari", when: "Sun 4:25 ET", away: "SEA", home: "ARI", line: "SEA −4.5" },
    { id: "was-dal", when: "Sun 4:25 ET", away: "WAS", home: "DAL", line: "DAL −4.5" },
    { id: "mia-sf", when: "Sun 4:25 ET", away: "MIA", home: "SF", line: "SF −13.5" },
    { id: "ind-kc", when: "Sun 8:20 ET", away: "IND", home: "KC", line: "KC −6.5" },
    { id: "nyg-lar", when: "Mon 8:15 ET", away: "NYG", home: "LAR", line: "LAR −7" }
  ];

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
      + '<img src="' + logoUrl(team) + '" alt="" width="28" height="28" />'
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
