import { fetchTowns } from ".";
import { writeFile } from "node:fs/promises";

fetchTowns().then((data) => {
  const names = data.groups.map((group) => group.uniqueName);
  writeFile(
    "src/towns.ts",
    `export type Town = ${names.map((name) => `"${name}"`).join(" | ")};`
  );
});
