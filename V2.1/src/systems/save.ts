import { SAVE_KEY, validateProgress, type Progress } from "./progression";

export function loadProgress(): Progress | null {
  const raw = window.localStorage.getItem(SAVE_KEY);
  if (!raw) return null;
  try {
    return validateProgress(JSON.parse(raw));
  } catch (error) {
    console.error("O salvamento V2 não contém JSON válido.", error);
    return null;
  }
}

export function saveProgress(progress: Progress): void {
  window.localStorage.setItem(SAVE_KEY, JSON.stringify(progress));
}

export function clearProgress(): void {
  window.localStorage.removeItem(SAVE_KEY);
}
