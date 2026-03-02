// Paste this entire block into the browser console on gabar.reliaguide.com
(async () => {
  const BASE = "/api/public/profiles?category.equals=Medical+Malpractice&categoryId.equals=454&memberTypeId.equals=1&size=20&page=";
  const FIELDS = ["First Name","Middle Name","Last Name","Firm Name","Firm Location","Office Phone","Cell Phone","Email"];

  const toRow = a => {
    const loc = a.primaryLocation || {};
    return [
      a.firstName   || "",
      a.middleName  || "",
      a.lastName    || "",
      a.firmName    || "",
      [loc.city, loc.region].filter(Boolean).join(", "),
      loc.phone     || "",
      loc.cell      || "",
      a.email       || "",
    ];
  };

  const escape = v => `"${String(v).replace(/"/g,'""')}"`;

  let rows = [FIELDS];
  let page = 0;
  while (true) {
    console.log(`Fetching page ${page}...`);
    const res  = await fetch(BASE + page);
    const data = await res.json();
    if (!data || data.length === 0) { console.log("Done."); break; }
    rows = rows.concat(data.map(toRow));
    console.log(`  → ${data.length} records (total: ${rows.length - 1})`);
    if (data.length < 20) break;
    page++;
    await new Promise(r => setTimeout(r, 400)); // polite delay
  }

  const csv  = rows.map(r => r.map(escape).join(",")).join("\r\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement("a");
  a.href = url; a.download = "medical_malpractice_georgia.csv"; a.click();
  URL.revokeObjectURL(url);
  console.log(`Downloaded ${rows.length - 1} attorneys.`);
})();
