import { describe, expect, it } from "vitest";
import { activateRune, newProgress, validateProgress, type Progress } from "../src/systems/progression";

describe("V2 progression", () => {
  it("requires the artifact, memory, and past state before the puzzle", () => {
    const progress = newProgress(20, 30);
    const result = activateRune(progress, "sun");

    expect(result.progress.puzzleIndex).toBe(0);
    expect(result.progress.puzzleSolved).toBe(false);
    expect(result.message).toContain("memória");
  });

  it("solves the symbols in order and opens the gate state", () => {
    let progress: Progress = {
      ...newProgress(20, 30),
      artifactAwakened: true,
      memoryRead: true,
      time: "past" as const,
    };

    for (const rune of ["sun", "moon", "wave"] as const) {
      progress = activateRune(progress, rune).progress;
    }

    expect(progress.puzzleIndex).toBe(3);
    expect(progress.puzzleSolved).toBe(true);
  });

  it("resets a wrong sequence without making the puzzle unwinnable", () => {
    const progress = {
      ...newProgress(20, 30),
      artifactAwakened: true,
      memoryRead: true,
      time: "past" as const,
      puzzleIndex: 1,
    };
    const result = activateRune(progress, "wave");

    expect(result.progress.puzzleIndex).toBe(0);
    expect(result.progress.puzzleSolved).toBe(false);
  });

  it("rejects malformed and non-V2 save data", () => {
    expect(validateProgress(null)).toBeNull();
    expect(validateProgress({ version: 1 })).toBeNull();
    expect(validateProgress({ ...newProgress(40, 50), x: Number.NaN })).toBeNull();
    expect(validateProgress(newProgress(40, 50))).toEqual(newProgress(40, 50));
  });
});
