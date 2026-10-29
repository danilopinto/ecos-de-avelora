import { WORLD, type TimeState } from "../data/phase";

export interface Progress {
  version: 2;
  x: number;
  y: number;
  time: TimeState;
  inscriptionRead: boolean;
  artifactAwakened: boolean;
  memoryRead: boolean;
  puzzleIndex: number;
  puzzleSolved: boolean;
  endingReached: boolean;
}

export const SAVE_KEY = "ecos-de-avelora-v2";
export const PUZZLE_SEQUENCE = ["sun", "moon", "wave"] as const;
export type RuneId = (typeof PUZZLE_SEQUENCE)[number];

export function newProgress(x: number, y: number): Progress {
  return {
    version: 2,
    x,
    y,
    time: "present",
    inscriptionRead: false,
    artifactAwakened: false,
    memoryRead: false,
    puzzleIndex: 0,
    puzzleSolved: false,
    endingReached: false,
  };
}

export function activateRune(progress: Progress, rune: RuneId): { progress: Progress; message: string } {
  if (!progress.artifactAwakened || !progress.memoryRead || progress.time !== "past") {
    return { progress, message: "A memória do passado precisa revelar a sequência primeiro." };
  }
  if (progress.puzzleSolved) return { progress, message: "Os três símbolos já estão ressoando." };

  const expected = PUZZLE_SEQUENCE[progress.puzzleIndex];
  if (rune !== expected) {
    return {
      progress: { ...progress, puzzleIndex: 0 },
      message: "A sequência se desfaz. A pista começa pelo Sol.",
    };
  }

  const puzzleIndex = progress.puzzleIndex + 1;
  const puzzleSolved = puzzleIndex === PUZZLE_SEQUENCE.length;
  return {
    progress: { ...progress, puzzleIndex, puzzleSolved },
    message: puzzleSolved ? "Sol, Lua e Ondas: a câmara se abriu." : `Símbolo ${puzzleIndex}/3 despertado.`,
  };
}

export function validateProgress(value: unknown): Progress | null {
  if (typeof value !== "object" || value === null) return null;
  const data = value as Partial<Progress>;
  if (
    data.version !== 2
    || typeof data.x !== "number" || !Number.isFinite(data.x) || data.x < 8 || data.x > WORLD.width - 8
    || typeof data.y !== "number" || !Number.isFinite(data.y) || data.y < 8 || data.y > WORLD.height - 8
    || (data.time !== "present" && data.time !== "past")
    || typeof data.inscriptionRead !== "boolean"
    || typeof data.artifactAwakened !== "boolean"
    || typeof data.memoryRead !== "boolean"
    || typeof data.puzzleSolved !== "boolean"
    || typeof data.endingReached !== "boolean"
    || typeof data.puzzleIndex !== "number"
    || !Number.isInteger(data.puzzleIndex)
    || data.puzzleIndex < 0 || data.puzzleIndex > 3
    || data.puzzleSolved !== (data.puzzleIndex === 3)
    || (data.artifactAwakened && !data.inscriptionRead)
    || (data.time === "past" && !data.artifactAwakened)
    || (data.memoryRead && !data.artifactAwakened)
    || (data.puzzleIndex > 0 && !data.memoryRead)
    || (data.endingReached && !data.puzzleSolved)
  ) return null;

  return data as Progress;
}
