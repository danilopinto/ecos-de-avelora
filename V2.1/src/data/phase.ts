export const VIEW = { width: 640, height: 360 } as const;
export const TILE_SIZE = 32;
export const MAP = { width: 50, height: 32 } as const;
export const WORLD = { width: MAP.width * TILE_SIZE, height: MAP.height * TILE_SIZE } as const;

export type TimeState = "present" | "past";

export interface Point {
  x: number;
  y: number;
}

export interface Interactable extends Point {
  id: "inscription" | "artifact" | "memory" | "sun" | "moon" | "wave" | "core";
  title: string;
  radius: number;
}

export const PLAYER_START: Point = { x: 420, y: 930 };
