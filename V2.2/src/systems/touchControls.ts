interface KeyDef {
  key: string;
  code: string;
  keyCode: number;
}

const KEYS: Record<string, KeyDef> = {
  left: { key: "ArrowLeft", code: "ArrowLeft", keyCode: 37 },
  up: { key: "ArrowUp", code: "ArrowUp", keyCode: 38 },
  right: { key: "ArrowRight", code: "ArrowRight", keyCode: 39 },
  down: { key: "ArrowDown", code: "ArrowDown", keyCode: 40 },
  space: { key: " ", code: "Space", keyCode: 32 },
  time: { key: "q", code: "KeyQ", keyCode: 81 },
};

// O Phaser lê keyCode em eventos de janela; por isso os botões emitem eventos de teclado sintéticos.
function dispatchKey(type: "keydown" | "keyup", def: KeyDef): void {
  const event = new KeyboardEvent(type, { key: def.key, code: def.code, bubbles: true, cancelable: true });
  Object.defineProperty(event, "keyCode", { get: () => def.keyCode });
  Object.defineProperty(event, "which", { get: () => def.keyCode });
  window.dispatchEvent(event);
}

export function isTouchDevice(): boolean {
  return window.matchMedia("(pointer: coarse)").matches || navigator.maxTouchPoints > 0;
}

export function setupTouchControls(root: HTMLElement): void {
  if (!isTouchDevice()) return;
  root.hidden = false;

  const pressedByPointer = new Map<number, string>();

  const release = (pointerId: number): void => {
    const name = pressedByPointer.get(pointerId);
    if (!name) return;
    pressedByPointer.delete(pointerId);
    const stillHeld = [...pressedByPointer.values()].includes(name);
    if (!stillHeld) dispatchKey("keyup", KEYS[name]);
  };

  root.querySelectorAll<HTMLButtonElement>("button[data-key]").forEach((button) => {
    const name = button.dataset.key ?? "";
    if (!KEYS[name]) return;

    button.addEventListener("pointerdown", (event) => {
      event.preventDefault();
      button.setPointerCapture(event.pointerId);
      pressedByPointer.set(event.pointerId, name);
      button.classList.add("is-pressed");
      dispatchKey("keydown", KEYS[name]);
    });

    const end = (event: PointerEvent): void => {
      release(event.pointerId);
      button.classList.remove("is-pressed");
    };
    button.addEventListener("pointerup", end);
    button.addEventListener("pointercancel", end);
    button.addEventListener("contextmenu", (event) => event.preventDefault());
  });
}
