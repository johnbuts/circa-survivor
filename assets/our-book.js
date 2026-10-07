(function () {
  window.CIRCA_BOOK = {
    week2: { TB: 5, SF: 3 },
    week3Live: [
      { id: "e04", n: 1, burned: ["JAC", "SF"], label: "04 JAC→SF" },
      { id: "e06", n: 1, burned: ["PIT", "SF"], label: "06 PIT→SF" },
      { id: "e10", n: 1, burned: ["LV", "SF"], label: "10 LV→SF" }
    ],
    // Week 3 and Week 4 picks were not recorded. Fill week5Live once they are,
    // e.g. { id: "e04", n: 1, burned: ["JAC", "SF", "KC", "MIN"], label: "04 …" }.
    week5Live: [],
    entries: [
      { id: 1, w1: { team: "JAC", opp: "CLE", result: "W" }, w2: { team: "TB", opp: "CLE", result: "L" }, live: false },
      { id: 2, w1: { team: "JAC", opp: "CLE", result: "W" }, w2: { team: "TB", opp: "CLE", result: "L" }, live: false },
      { id: 3, w1: { team: "JAC", opp: "CLE", result: "W" }, w2: { team: "TB", opp: "CLE", result: "L" }, live: false },
      { id: 4, w1: { team: "JAC", opp: "CLE", result: "W" }, w2: { team: "SF", opp: "MIA", result: "W" }, live: true, slot: "e04" },
      { id: 5, w1: { team: "PIT", opp: "ATL", result: "W" }, w2: { team: "TB", opp: "CLE", result: "L" }, live: false },
      { id: 6, w1: { team: "PIT", opp: "ATL", result: "W" }, w2: { team: "SF", opp: "MIA", result: "W" }, live: true, slot: "e06" },
      { id: 7, w1: { team: "TEN", opp: "NYJ", result: "L" }, w2: null, live: false },
      { id: 8, w1: { team: "TEN", opp: "NYJ", result: "L" }, w2: null, live: false },
      { id: 9, w1: { team: "LV", opp: "MIA", result: "W" }, w2: { team: "TB", opp: "CLE", result: "L" }, live: false },
      { id: 10, w1: { team: "LV", opp: "MIA", result: "W" }, w2: { team: "SF", opp: "MIA", result: "W" }, live: true, slot: "e10" }
    ]
  };
})();
