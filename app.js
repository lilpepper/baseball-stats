const stats = [
  {
    player: "Barry Bonds",
    year: 2001,
    team: "SF",
    type: "batting",
    hr: 73,
    rbi: 137,
    avg: 0.328,
    obp: 0.515,
    slg: 0.863,
    ops: 1.378,
    notes: "Single-season HR record.",
  },
  {
    player: "Babe Ruth",
    year: 1927,
    team: "NYY",
    type: "batting",
    hr: 60,
    rbi: 165,
    avg: 0.356,
    obp: 0.486,
    slg: 0.772,
    ops: 1.258,
    notes: "Murderers' Row peak.",
  },
  {
    player: "Hank Aaron",
    year: 1957,
    team: "MLB",
    type: "batting",
    hr: 44,
    rbi: 132,
    avg: 0.322,
    obp: 0.378,
    slg: 0.600,
    ops: 0.978,
    notes: "MVP season, Braves title.",
  },
  {
    player: "Willie Mays",
    year: 1954,
    team: "NYG",
    type: "batting",
    hr: 41,
    rbi: 110,
    avg: 0.345,
    obp: 0.411,
    slg: 0.667,
    ops: 1.078,
    notes: "Say Hey MVP campaign.",
  },
  {
    player: "Ken Griffey Jr.",
    year: 1997,
    team: "SEA",
    type: "batting",
    hr: 56,
    rbi: 147,
    avg: 0.304,
    obp: 0.382,
    slg: 0.646,
    ops: 1.028,
    notes: "Back-to-back 56 HRs.",
  },
  {
    player: "Shohei Ohtani",
    year: 2023,
    team: "LAA",
    type: "batting",
    hr: 44,
    rbi: 95,
    avg: 0.304,
    obp: 0.412,
    slg: 0.654,
    ops: 1.066,
    notes: "MVP two-way dominance.",
  },
  {
    player: "Mookie Betts",
    year: 2018,
    team: "BOS",
    type: "batting",
    hr: 32,
    rbi: 80,
    avg: 0.346,
    obp: 0.438,
    slg: 0.640,
    ops: 1.078,
    notes: "AL MVP and World Series.",
  },
  {
    player: "Mickey Mantle",
    year: 1956,
    team: "NYY",
    type: "batting",
    hr: 52,
    rbi: 130,
    avg: 0.353,
    obp: 0.464,
    slg: 0.705,
    ops: 1.169,
    notes: "Triple Crown.",
  },
  {
    player: "Bob Gibson",
    year: 1968,
    team: "STL",
    type: "pitching",
    era: 1.12,
    wins: 22,
    so: 268,
    whip: 0.853,
    notes: "Year of the Pitcher." ,
  },
  {
    player: "Pedro Martinez",
    year: 2000,
    team: "BOS",
    type: "pitching",
    era: 1.74,
    wins: 18,
    so: 284,
    whip: 0.737,
    notes: "Peak dominance in the AL.",
  },
  {
    player: "Sandy Koufax",
    year: 1965,
    team: "LAD",
    type: "pitching",
    era: 2.04,
    wins: 26,
    so: 382,
    whip: 0.855,
    notes: "Cy Young and MVP.",
  },
  {
    player: "Mariano Rivera",
    year: 1996,
    team: "NYY",
    type: "pitching",
    era: 2.09,
    wins: 8,
    so: 107,
    whip: 0.983,
    notes: "Historic setup season.",
  },
  {
    player: "Jacob deGrom",
    year: 2018,
    team: "NYM",
    type: "pitching",
    era: 1.70,
    wins: 10,
    so: 269,
    whip: 0.912,
    notes: "Cy Young with elite strikeouts.",
  },
  {
    player: "Greg Maddux",
    year: 1995,
    team: "ATL",
    type: "pitching",
    era: 1.63,
    wins: 19,
    so: 181,
    whip: 0.811,
    notes: "Command masterclass.",
  },
];

const elements = {
  resultsGrid: document.getElementById("results-grid"),
  resultCount: document.getElementById("result-count"),
  hrRange: document.getElementById("hr-range"),
  hrValue: document.getElementById("hr-value"),
  avgRange: document.getElementById("avg-range"),
  avgValue: document.getElementById("avg-value"),
  eraRange: document.getElementById("era-range"),
  eraValue: document.getElementById("era-value"),
  startYear: document.getElementById("start-year"),
  endYear: document.getElementById("end-year"),
  typeButtons: document.querySelectorAll(".pill"),
  resetButton: document.getElementById("reset-filters"),
  queryInput: document.getElementById("query-input"),
  runQuery: document.getElementById("run-query"),
  queryResponse: document.getElementById("query-response"),
};

let activeType = "all";

const formatAverage = (value) => value.toFixed(3).replace("0.", ".");

const filters = {
  hr: Number(elements.hrRange.value),
  avg: Number(elements.avgRange.value),
  era: Number(elements.eraRange.value),
  startYear: Number(elements.startYear.value),
  endYear: Number(elements.endYear.value),
};

const updateDialLabels = () => {
  elements.hrValue.textContent = filters.hr;
  elements.avgValue.textContent = formatAverage(filters.avg);
  elements.eraValue.textContent = filters.era.toFixed(2);
};

const filterStats = () =>
  stats.filter((entry) => {
    if (activeType !== "all" && entry.type !== activeType) return false;
    if (entry.year < filters.startYear || entry.year > filters.endYear) return false;
    if (entry.type === "batting") {
      return entry.hr >= filters.hr && entry.avg >= filters.avg;
    }
    return entry.era <= filters.era;
  });

const renderResults = () => {
  const filtered = filterStats();
  elements.resultsGrid.innerHTML = filtered
    .map((entry) => {
      const isBatting = entry.type === "batting";
      return `
      <article class="result-card">
        <span class="tag ${entry.type}">${isBatting ? "Batting" : "Pitching"}</span>
        <h4>${entry.player} · ${entry.year}</h4>
        <p class="muted">${entry.team} • ${entry.notes}</p>
        <div class="stat-grid">
          ${
            isBatting
              ? `
                <div class="stat"><strong>${entry.hr}</strong><span>HR</span></div>
                <div class="stat"><strong>${entry.rbi}</strong><span>RBI</span></div>
                <div class="stat"><strong>${formatAverage(entry.avg)}</strong><span>AVG</span></div>
                <div class="stat"><strong>${entry.ops.toFixed(3)}</strong><span>OPS</span></div>
              `
              : `
                <div class="stat"><strong>${entry.era.toFixed(2)}</strong><span>ERA</span></div>
                <div class="stat"><strong>${entry.wins}</strong><span>Wins</span></div>
                <div class="stat"><strong>${entry.so}</strong><span>SO</span></div>
                <div class="stat"><strong>${entry.whip.toFixed(3)}</strong><span>WHIP</span></div>
              `
          }
        </div>
      </article>
    `;
    })
    .join("");

  elements.resultCount.textContent = filtered.length.toString();
};

const updateFilter = (key, value) => {
  filters[key] = Number(value);
  updateDialLabels();
  renderResults();
};

const resetFilters = () => {
  activeType = "all";
  filters.hr = 30;
  filters.avg = 0.3;
  filters.era = 3.5;
  filters.startYear = 1940;
  filters.endYear = 2023;

  elements.hrRange.value = filters.hr;
  elements.avgRange.value = filters.avg;
  elements.eraRange.value = filters.era;
  elements.startYear.value = filters.startYear;
  elements.endYear.value = filters.endYear;

  elements.typeButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.type === "all");
  });

  updateDialLabels();
  renderResults();
};

const runQuery = () => {
  const input = elements.queryInput.value.trim().toLowerCase();
  if (!input) {
    elements.queryResponse.innerHTML = "<p class=\"muted\">Add a query to get tailored insights.</p>";
    return;
  }

  const mentionsPitching = /pitch|era|whip|strikeout|so/.test(input);
  const mentionsBatting = /hr|home run|slug|ops|avg|batting/.test(input);
  const minHrMatch = input.match(/(\d{2,})\s*\+?\s*hr/);
  const minEraMatch = input.match(/era\s*under\s*(\d\.\d{1,2})/);
  const targetTeam = stats.find((entry) => input.includes(entry.team.toLowerCase()));

  let responseType = "all";
  if (mentionsPitching && !mentionsBatting) responseType = "pitching";
  if (mentionsBatting && !mentionsPitching) responseType = "batting";

  if (minHrMatch) {
    filters.hr = Math.max(filters.hr, Number(minHrMatch[1]));
    elements.hrRange.value = filters.hr;
  }

  if (minEraMatch) {
    filters.era = Math.min(filters.era, Number(minEraMatch[1]));
    elements.eraRange.value = filters.era;
  }

  if (targetTeam) {
    filters.startYear = Math.min(filters.startYear, targetTeam.year);
    filters.endYear = Math.max(filters.endYear, targetTeam.year);
    elements.startYear.value = filters.startYear;
    elements.endYear.value = filters.endYear;
  }

  if (responseType !== "all") {
    activeType = responseType;
    elements.typeButtons.forEach((button) => {
      button.classList.toggle("active", button.dataset.type === activeType);
    });
  }

  updateDialLabels();
  renderResults();

  const filtered = filterStats();
  const highlight = filtered.slice(0, 3);
  const insight = highlight
    .map((entry) => `${entry.player} (${entry.year})`)
    .join(", ");

  elements.queryResponse.innerHTML = `
    <p><strong>Query interpreted:</strong> ${input}</p>
    <p><strong>Suggested filters:</strong> Type: ${activeType}, HR ≥ ${filters.hr}, AVG ≥ ${formatAverage(
      filters.avg
    )}, ERA ≤ ${filters.era.toFixed(2)}</p>
    <p><strong>Top matches:</strong> ${insight || "No matching seasons yet."}</p>
  `;
};

elements.hrRange.addEventListener("input", (event) => updateFilter("hr", event.target.value));
elements.avgRange.addEventListener("input", (event) => updateFilter("avg", event.target.value));
elements.eraRange.addEventListener("input", (event) => updateFilter("era", event.target.value));
elements.startYear.addEventListener("input", (event) => updateFilter("startYear", event.target.value));
elements.endYear.addEventListener("input", (event) => updateFilter("endYear", event.target.value));

Array.from(elements.typeButtons).forEach((button) => {
  button.addEventListener("click", () => {
    activeType = button.dataset.type;
    elements.typeButtons.forEach((pill) => {
      pill.classList.toggle("active", pill === button);
    });
    renderResults();
  });
});

elements.resetButton.addEventListener("click", resetFilters);
elements.runQuery.addEventListener("click", runQuery);

updateDialLabels();
renderResults();
