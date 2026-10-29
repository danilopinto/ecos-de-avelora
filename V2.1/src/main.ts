import Phaser from "phaser";
import { ExplorationScene } from "./scenes/ExplorationScene";
import "./style.css";
import { loadProgress } from "./systems/save";
import { VIEW } from "./data/phase";

const menu = document.querySelector<HTMLElement>("#menu");
const pauseScreen = document.querySelector<HTMLElement>("#pause-screen");
const endingScreen = document.querySelector<HTMLElement>("#ending-screen");
const continueButton = document.querySelector<HTMLButtonElement>("#continue-game");
const status = document.querySelector<HTMLElement>("#status");
const host = document.querySelector<HTMLElement>("#game-container");

if (!menu || !pauseScreen || !endingScreen || !continueButton || !status || !host) {
  throw new Error("A interface da V2 está incompleta: faltam elementos obrigatórios do documento.");
}

const ui = { menu, pauseScreen, endingScreen, continueButton, status };
let game: Phaser.Game | null = null;

function createGame(initialMode: "menu" | "new" | "continue"): Phaser.Game {
  if (game) return game;
  game = new Phaser.Game({
    type: Phaser.AUTO,
    parent: host,
    width: VIEW.width,
    height: VIEW.height,
    backgroundColor: "#152b26",
    pixelArt: true,
    roundPixels: true,
    antialias: false,
    banner: false,
    scale: {
      mode: Phaser.Scale.FIT,
      autoCenter: Phaser.Scale.CENTER_BOTH,
      width: VIEW.width,
      height: VIEW.height,
    },
    physics: {
      default: "arcade",
      arcade: { debug: false },
    },
    scene: [new ExplorationScene(ui, initialMode)],
  });
  return game;
}

function startNewGame(): void {
  const instance = game ?? createGame("new");
  ui.menu.hidden = true;
  ui.pauseScreen.hidden = true;
  ui.endingScreen.hidden = true;
  if (game === instance && instance.scene.isActive("Exploration")) instance.events.emit("game:new");
  ui.status.textContent = "A jornada começou. Explore as ruínas.";
}

document.querySelector("#new-game")?.addEventListener("click", startNewGame);
continueButton.addEventListener("click", () => {
  const instance = game ?? createGame("continue");
  ui.menu.hidden = true;
  if (game === instance && instance.scene.isActive("Exploration")) instance.events.emit("game:continue");
});
document.querySelector("#resume-game")?.addEventListener("click", () => game?.events.emit("game:resume"));
document.querySelector("#restart-game")?.addEventListener("click", startNewGame);
document.querySelector("#return-menu")?.addEventListener("click", () => {
  game?.events.emit("game:pause");
  ui.pauseScreen.hidden = true;
  ui.menu.hidden = false;
});
document.querySelector("#ending-menu")?.addEventListener("click", () => {
  ui.endingScreen.hidden = true;
  ui.menu.hidden = false;
  game?.events.emit("game:pause");
});
document.querySelector("#ending-restart")?.addEventListener("click", startNewGame);

try {
  continueButton.hidden = loadProgress() === null;
} catch (error) {
  console.error("Não foi possível verificar o salvamento local da V2.", error);
  continueButton.hidden = true;
  ui.status.textContent = "O armazenamento local não está disponível; uma nova jornada ainda pode ser iniciada.";
}
