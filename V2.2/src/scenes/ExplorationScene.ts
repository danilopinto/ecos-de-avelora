import Phaser from "phaser";
import {
  PLAYER_START,
  TILE_SIZE,
  VIEW,
  WORLD,
  type Interactable,
  type Point,
  type TimeState,
} from "../data/phase";
import {
  activateRune,
  newProgress,
  type Progress,
} from "../systems/progression";
import { loadProgress, saveProgress } from "../systems/save";

type LightTone = "warm" | "cyan";

interface LightSource {
  x: number;
  y: number;
  radius: number;
  strength: number;
  tone: LightTone;
  seed: number;
  glow: Phaser.GameObjects.Image;
  flicker: number;
  enabled?: () => boolean;
}

interface DecorEntry {
  f: string;
  x: number;
  y: number;
  c?: [number, number];
  c2?: [number, number, number][];
  l?: [number, LightTone];
}

const TONE_TINT: Record<LightTone, { glow: number; alpha: number }> = {
  warm: { glow: 0xffa24a, alpha: 0.2 },
  cyan: { glow: 0x4fe0d4, alpha: 0.17 },
};
const RUNE_ORDER = ["sun", "moon", "wave"] as const;

interface UiElements {
  menu: HTMLElement;
  pauseScreen: HTMLElement;
  endingScreen: HTMLElement;
  continueButton: HTMLButtonElement;
  status: HTMLElement;
}

export class ExplorationScene extends Phaser.Scene {
  private progress: Progress = newProgress(PLAYER_START.x, PLAYER_START.y);
  private playerStart: Point = PLAYER_START;
  private interactables: Interactable[] = [];
  private player!: Phaser.Physics.Arcade.Sprite;
  private obstacles!: Phaser.Physics.Arcade.StaticGroup;
  private streamBlockers: Phaser.GameObjects.GameObject[] = [];
  private map!: Phaser.Tilemaps.Tilemap;
  private prompt!: Phaser.GameObjects.Text;
  private dialogueBox!: Phaser.GameObjects.Container;
  private interactionKey!: Phaser.Input.Keyboard.Key;
  private timeKey!: Phaser.Input.Keyboard.Key;
  private pauseKey!: Phaser.Input.Keyboard.Key;
  private spaceKey!: Phaser.Input.Keyboard.Key;
  private enterKey!: Phaser.Input.Keyboard.Key;
  private cursorKeys!: Phaser.Types.Input.Keyboard.CursorKeys;
  private movementKeys!: Record<"w" | "a" | "s" | "d", Phaser.Input.Keyboard.Key>;
  private statusText!: Phaser.GameObjects.Text;
  private ui: UiElements;
  private paused = true;
  private saveClock = 0;
  private activeDialogue = false;
  private dialogueLines: string[] = [];
  private dialogueIndex = 0;
  private noticeUntil = 0;
  private doorBlocker!: Phaser.GameObjects.GameObject;
  private darkness!: Phaser.GameObjects.RenderTexture;
  private lightStamp!: Phaser.GameObjects.Image;
  private lightSources: LightSource[] = [];
  private playerLight!: LightSource;
  private specialLights: Partial<Record<"artifact" | "core" | "inscription", LightSource>> = {};
  private runeSprites: Partial<Record<"sun" | "moon" | "wave", Phaser.GameObjects.Image>> = {};
  private echoSprite?: Phaser.GameObjects.Image;
  private doorSeal?: Phaser.GameObjects.Image;

  private isInteractableId(name: string): name is Interactable["id"] {
    return name === "inscription" || name === "artifact" || name === "memory"
      || name === "sun" || name === "moon" || name === "wave" || name === "core";
  }

  constructor(ui: UiElements, private initialMode: "menu" | "new" | "continue" = "menu") {
    super("Exploration");
    this.ui = ui;
  }

  preload(): void {
    this.load.image("avelora-tiles", "assets/tiles/avelora-tiles.png");
    this.load.tilemapTiledJSON("forest-map", "maps/fase-01/forest.json");
    this.load.spritesheet("player", "assets/sprites/player.png", { frameWidth: 32, frameHeight: 48 });
    this.load.atlas("decor", "assets/sprites/decor.png", "assets/sprites/decor.json");
    this.load.image("light", "assets/sprites/light.png");
    this.load.json("decor-layout", "maps/fase-01/decor.json");
    this.load.on("loaderror", (file: Phaser.Loader.File) => {
      console.error(`Falha ao carregar asset da V2: ${file.key} (${file.src})`);
      this.ui.status.textContent = `Não foi possível carregar o recurso "${file.key}". Confira os arquivos da V2.`;
    });
  }

  create(): void {
    this.map = this.make.tilemap({ key: "forest-map" });
    const objectLayer = this.map.getObjectLayer("Objects");
    const spawn = objectLayer?.objects.find(object => object.name === "spawn");
    if (spawn && typeof spawn.x === "number" && typeof spawn.y === "number") {
      this.playerStart = { x: spawn.x, y: spawn.y };
    }
    const tileset = this.map.addTilesetImage("Avelora", "avelora-tiles", TILE_SIZE, TILE_SIZE, 0, 0);
    if (!tileset) throw new Error("Não foi possível associar o tileset Avelora ao mapa da V2.");
    const ground = this.map.createLayer("Ground", tileset, 0, 0);
    const details = this.map.createLayer("GroundDetails", tileset, 0, 0);
    const water = this.map.createLayer("Water", tileset, 0, 0);
    const path = this.map.createLayer("Path", tileset, 0, 0);
    const ruins = this.map.createLayer("Architecture", tileset, 0, 0);
    if (!ground || !details || !water || !path || !ruins) {
      throw new Error("O mapa da Fase 1 está sem uma ou mais camadas obrigatórias.");
    }
    ground.setDepth(0);
    details.setDepth(1);
    water.setDepth(2);
    path.setDepth(3);
    ruins.setDepth(4);
    this.physics.world.setBounds(0, 0, WORLD.width, WORLD.height);

    this.obstacles = this.physics.add.staticGroup();
    this.createLightingLayer();
    this.createShrine();
    this.createDecor();
    this.createInteractables();
    this.createPlayer();
    this.createHud();
    this.createAnimations();
    this.physics.add.collider(this.player, this.obstacles);
    this.cameras.main.setBounds(0, 0, WORLD.width, WORLD.height);
    this.cameras.main.setRoundPixels(true);
    this.events.on(Phaser.Scenes.Events.POST_UPDATE, this.followAndLight, this);

    const keyboard = this.input.keyboard;
    if (!keyboard) throw new Error("A V2 precisa de suporte a teclado para os controles atuais.");
    this.interactionKey = keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.E);
    this.timeKey = keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.Q);
    this.pauseKey = keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ESC);
    this.spaceKey = keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    this.enterKey = keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ENTER);
    this.cursorKeys = keyboard.createCursorKeys();
    this.movementKeys = {
      w: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),
      a: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
      s: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),
      d: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D),
    };
    keyboard.addCapture([
      Phaser.Input.Keyboard.KeyCodes.UP,
      Phaser.Input.Keyboard.KeyCodes.DOWN,
      Phaser.Input.Keyboard.KeyCodes.LEFT,
      Phaser.Input.Keyboard.KeyCodes.RIGHT,
      Phaser.Input.Keyboard.KeyCodes.SPACE,
    ]);
    this.game.events.on("game:new", this.startNew, this);
    this.game.events.on("game:continue", this.continueGame, this);
    this.game.events.on("game:resume", this.resumeGame, this);
    this.game.events.on("game:pause", this.pauseGame, this);
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, this.cleanup, this);
    this.followAndLight();

    this.progress = newProgress(this.playerStart.x, this.playerStart.y);
    this.updatePrompt();
    this.syncWorldState();
    if (this.initialMode === "new") this.startNew();
    if (this.initialMode === "continue") this.continueGame();
  }

  update(_time: number, delta: number): void {
    if (!this.player || this.paused) return;
    if (this.activeDialogue) {
      if (Phaser.Input.Keyboard.JustDown(this.pauseKey)) {
        this.pauseGame();
        return;
      }
      if (
        Phaser.Input.Keyboard.JustDown(this.interactionKey)
        || Phaser.Input.Keyboard.JustDown(this.spaceKey)
        || Phaser.Input.Keyboard.JustDown(this.enterKey)
      ) this.handleInteraction();
      return;
    }
    const left = this.cursorKeys.left.isDown || this.movementKeys.a.isDown;
    const right = this.cursorKeys.right.isDown || this.movementKeys.d.isDown;
    const up = this.cursorKeys.up.isDown || this.movementKeys.w.isDown;
    const down = this.cursorKeys.down.isDown || this.movementKeys.s.isDown;
    let dx = Number(right) - Number(left);
    let dy = Number(down) - Number(up);
    if (dx !== 0 && dy !== 0) {
      dx *= Math.SQRT1_2;
      dy *= Math.SQRT1_2;
    }
    const speed = 118;
    this.player.setVelocity(dx * speed, dy * speed);
    this.player.setDepth(this.player.y + 40);
    if (dx || dy) {
      const direction = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 1 : 2) : (dy > 0 ? 0 : 3);
      this.player.setData("direction", direction);
      this.player.anims.play(`walk-${direction}`, true);
    } else {
      this.player.anims.stop();
      this.player.setFrame(Number(this.player.getData("direction")) * 4 + 1);
    }

    if (Phaser.Input.Keyboard.JustDown(this.interactionKey)) this.handleInteraction();
    if (Phaser.Input.Keyboard.JustDown(this.spaceKey) || Phaser.Input.Keyboard.JustDown(this.enterKey)) this.handleInteraction();
    if (Phaser.Input.Keyboard.JustDown(this.timeKey)) this.toggleTime();
    if (Phaser.Input.Keyboard.JustDown(this.pauseKey)) this.pauseGame();
    this.updatePrompt();
    this.saveClock += delta;
    if (this.saveClock >= 2500) {
      this.saveClock = 0;
      this.persist();
    }
    if (this.noticeUntil && performance.now() > this.noticeUntil) {
      this.statusText.setText("");
      this.noticeUntil = 0;
    }
  }

  private addObstacle(x: number, y: number, width: number, height: number): Phaser.GameObjects.GameObject {
    const obstacle = this.add.rectangle(x + width / 2, y + height / 2, width, height, 0x000000, 0);
    this.obstacles.add(obstacle);
    return obstacle;
  }

  private addLight(x: number, y: number, radius: number, tone: LightTone, strength = 1, flicker = 0.05): LightSource {
    const glow = this.add.image(x, y, "light")
      .setDepth(2510)
      .setBlendMode(Phaser.BlendModes.ADD)
      .setTint(TONE_TINT[tone].glow);
    const light: LightSource = { x, y, radius, strength, tone, seed: this.lightSources.length * 1.7, glow, flicker };
    this.lightSources.push(light);
    return light;
  }

  private createLightingLayer(): void {
    this.darkness = this.add.renderTexture(0, 0, VIEW.width, VIEW.height)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(2500);
    this.lightStamp = this.make.image({ key: "light", add: false });
  }

  private createShrine(): void {
    this.add.image(672, 112, "decor", "shrine_back").setOrigin(0, 0).setDepth(5);
    this.add.image(720, 344, "decor", "shrine_front").setOrigin(0, 0).setDepth(424);
    this.doorSeal = this.add.image(800, 364, "decor", "seal").setDepth(425).setBlendMode(Phaser.BlendModes.ADD);
    this.addObstacle(672, 112, 48, 272);
    this.addObstacle(880, 112, 48, 272);
    this.addObstacle(720, 112, 160, 48);
    this.addObstacle(720, 344, 50, 40);
    this.addObstacle(830, 344, 50, 40);
    this.doorBlocker = this.addObstacle(770, 344, 60, 40);
    for (const x of [738, 862]) {
      this.add.image(x, 338, "decor", "torch").setOrigin(0.5, 1).setDepth(378);
      this.addObstacle(x - 7, 330, 14, 8);
      this.addLight(x, 292, 120, "warm", 0.95, 0.07);
    }
  }

  private createDecor(): void {
    const layout = (this.cache.json.get("decor-layout") ?? []) as DecorEntry[];
    for (const entry of layout) {
      const isLily = entry.f.startsWith("lily");
      const sprite = this.add.image(entry.x, entry.y, "decor", entry.f).setOrigin(0.5, 1);
      sprite.setDepth(isLily ? 2.5 : entry.y + 40);
      if (entry.c) this.addObstacle(entry.x - entry.c[0] / 2, entry.y - entry.c[1], entry.c[0], entry.c[1]);
      for (const [dx, w, h] of entry.c2 ?? []) this.addObstacle(entry.x + dx - w / 2, entry.y - h, w, h);
      if (entry.l) {
        const [radius, tone] = entry.l;
        const lift = entry.f === "torch" ? 48 : 20;
        const light = this.addLight(entry.x, entry.y - lift, radius, tone, tone === "warm" ? 0.95 : 0.8, tone === "warm" ? 0.07 : 0.02);
        light.seed += entry.x * 0.013;
      }
    }
  }

  private createInteractables(): void {
    const objects = this.map.getObjectLayer("Objects")?.objects ?? [];
    const titles: Record<Interactable["id"], string> = {
      inscription: "Ler a inscrição",
      artifact: "Despertar o cristal",
      memory: "Examinar a memória",
      sun: "Ativar o símbolo do Sol",
      moon: "Ativar o símbolo da Lua",
      wave: "Ativar o símbolo das Ondas",
      core: "Abrir a câmara",
    };
    const radius: Record<Interactable["id"], number> = {
      inscription: 38, artifact: 42, memory: 42, sun: 38, moon: 38, wave: 38, core: 46,
    };
    for (const point of objects) {
      if (
        point.type !== "interaction"
        || !this.isInteractableId(point.name)
        || typeof point.x !== "number"
        || typeof point.y !== "number"
      ) continue;
      const object: Interactable = {
        id: point.name,
        title: titles[point.name],
        x: point.x,
        y: point.y,
        radius: radius[point.name],
      };
      this.interactables.push(object);
      this.createInteractableSprite(object);
    }
  }

  private createInteractableSprite(object: Interactable): void {
    const { x, y } = object;
    const stand = (frame: string, baseY: number, w: number, h: number) => {
      const sprite = this.add.image(x, baseY, "decor", frame).setOrigin(0.5, 1).setDepth(baseY + 40);
      this.addObstacle(x - w / 2, baseY - h, w, h);
      return sprite;
    };
    if (object.id === "inscription") {
      stand("slab", y + 10, 22, 8);
      this.specialLights.inscription = this.addLight(x, y - 20, 56, "cyan", 0.5, 0.03);
    } else if (object.id === "artifact") {
      stand("artifact", y + 10, 26, 10);
      this.specialLights.artifact = this.addLight(x, y - 26, 62, "cyan", 0.45, 0.03);
    } else if (object.id === "memory") {
      this.echoSprite = this.add.image(x, y, "decor", "echo").setDepth(y + 40).setBlendMode(Phaser.BlendModes.ADD);
      this.tweens.add({ targets: this.echoSprite, y: y - 5, duration: 1500, yoyo: true, repeat: -1, ease: "Sine.easeInOut" });
      const light = this.addLight(x, y, 84, "cyan", 0.9, 0.04);
      light.enabled = () => this.progress.time === "past" && !this.progress.memoryRead;
    } else if (object.id === "core") {
      stand("core", y + 15, 30, 12);
      this.specialLights.core = this.addLight(x, y - 12, 90, "cyan", 0.55, 0.03);
    } else {
      this.runeSprites[object.id] = stand(`rune_${object.id}`, y + 8, 12, 10);
      const index = RUNE_ORDER.indexOf(object.id);
      const light = this.addLight(x, y - 16, 56, "cyan", 0.9, 0.03);
      light.enabled = () => this.runeLit(index);
    }
  }

  private runeLit(index: number): boolean {
    return this.progress.puzzleSolved || this.progress.puzzleIndex > index;
  }

  private createPlayer(): void {
    this.player = this.physics.add.sprite(this.playerStart.x, this.playerStart.y, "player", 1);
    this.player.setOrigin(0.5, 0.85);
    this.player.setDepth(this.player.y + 40);
    this.player.setCollideWorldBounds(true);
    this.player.body?.setSize(18, 14).setOffset(7, 32);
    this.player.setData("direction", 0);
    this.playerLight = this.addLight(this.player.x, this.player.y - 14, 132, "warm", 1, 0.045);
  }

  private createHud(): void {
    const camera = this.cameras.main;
    this.add.rectangle(320, 21, 620, 34, 0x10211d, 0.92).setScrollFactor(0).setDepth(3000);
    this.add.text(17, 10, "AVELORA  ·  A FLORESTA ESQUECIDA", {
      fontFamily: "monospace", fontSize: "11px", color: "#e6ebd6", fontStyle: "bold",
    }).setScrollFactor(0).setDepth(3001);
    this.statusText = this.add.text(18, 29, "", {
      fontFamily: "monospace", fontSize: "10px", color: "#f0cf89",
    }).setScrollFactor(0).setDepth(3001);
    this.prompt = this.add.text(320, 335, "", {
      fontFamily: "monospace", fontSize: "11px", color: "#f3efd9",
      backgroundColor: "#10211de8", padding: { x: 8, y: 5 },
    }).setOrigin(0.5).setScrollFactor(0).setDepth(3001);
    this.dialogueBox = this.add.container(320, 300).setScrollFactor(0).setDepth(3100).setVisible(false);
    const panel = this.add.rectangle(0, 0, 600, 94, 0x101b18, 0.98).setStrokeStyle(2, 0x92bd8f);
    const title = this.add.text(-282, -35, "", {
      fontFamily: "monospace", fontSize: "13px", color: "#aee0b4", fontStyle: "bold",
      wordWrap: { width: 560 },
    }).setName("dialogue-title");
    const body = this.add.text(-282, -13, "", {
      fontFamily: "monospace", fontSize: "12px", color: "#eef0db", lineSpacing: 5,
      wordWrap: { width: 560 },
    }).setName("dialogue-body");
    const next = this.add.text(277, 31, "E  continuar ▶", {
      fontFamily: "monospace", fontSize: "10px", color: "#f0cf89",
    }).setOrigin(1, 0.5);
    this.dialogueBox.add([panel, title, body, next]);
    camera.setZoom(1);
  }

  private createAnimations(): void {
    for (let direction = 0; direction < 4; direction += 1) {
      this.anims.create({
        key: `walk-${direction}`,
        frames: this.anims.generateFrameNumbers("player", { frames: [0, 1, 2, 3].map(step => direction * 4 + step) }),
        frameRate: 8,
        repeat: -1,
      });
    }
  }

  private followAndLight(): void {
    if (!this.player) return;
    const camera = this.cameras.main;
    camera.setScroll(
      Math.round(Phaser.Math.Clamp(this.player.x - VIEW.width / 2, 0, WORLD.width - VIEW.width)),
      Math.round(Phaser.Math.Clamp(this.player.y - VIEW.height / 2, 0, WORLD.height - VIEW.height)),
    );
    const side = this.player.getData("direction") === 1 ? 5 : this.player.getData("direction") === 2 ? -5 : 0;
    this.playerLight.x = Math.round(this.player.x + side);
    this.playerLight.y = Math.round(this.player.y - 14);
    this.doorSeal?.setAlpha(0.55 + Math.sin(this.time.now / 260) * 0.2);
    this.renderLighting();
  }

  private renderLighting(): void {
    const camera = this.cameras.main;
    const past = this.progress.time === "past";
    const now = this.time.now;
    this.darkness.clear();
    this.darkness.fill(past ? 0x082a2e : 0x040a12, past ? 0.58 : 0.8);
    for (const light of this.lightSources) {
      const screenX = Math.round(light.x - camera.scrollX);
      const screenY = Math.round(light.y - camera.scrollY);
      const visible = (!light.enabled || light.enabled())
        && screenX > -light.radius && screenX < VIEW.width + light.radius
        && screenY > -light.radius && screenY < VIEW.height + light.radius;
      light.glow.setVisible(visible);
      if (!visible) continue;
      const wobble = 1 + light.flicker * (Math.sin(now / 90 + light.seed * 5) * 0.6 + Math.sin(now / 37 + light.seed * 11) * 0.4);
      const radius = Math.round(light.radius * wobble);
      this.lightStamp.setScale((radius * 2) / 256).setAlpha(Math.min(1, light.strength));
      this.darkness.erase(this.lightStamp, screenX, screenY);
      const tone = TONE_TINT[light.tone];
      light.glow
        .setPosition(light.x, light.y)
        .setScale((radius * 1.5) / 256)
        .setAlpha(tone.alpha * Math.min(1, light.strength) * (past ? 0.8 : 1));
    }
  }

  private nearestInteractable(): Interactable | null {
    if (!this.player) return null;
    let closest: Interactable | null = null;
    let best = Infinity;
    for (const target of this.interactables) {
      const distance = Phaser.Math.Distance.Between(this.player.x, this.player.y, target.x, target.y);
      if (distance <= target.radius && distance < best) {
        closest = target;
        best = distance;
      }
    }
    return closest;
  }

  private updatePrompt(): void {
    const target = this.nearestInteractable();
    const text = target ? `E  ${target.title}` : this.activeDialogue ? "E  continuar" : "";
    this.prompt.setText(text);
    this.prompt.setVisible(!this.paused && Boolean(text) && !this.activeDialogue);
    const timeLabel = this.progress.time === "past" ? "PASSADO" : "PRESENTE";
    this.statusText.setText(`${timeLabel}  ·  ${this.objective()}`);
  }

  private objective(): string {
    if (!this.progress.inscriptionRead) return "Leia a inscrição antiga";
    if (!this.progress.artifactAwakened) return "Desperte o cristal";
    if (!this.progress.memoryRead) return "Encontre o eco na ponte";
    if (!this.progress.puzzleSolved) return `Ative Sol → Lua → Ondas  (${this.progress.puzzleIndex}/3)`;
    if (!this.progress.endingReached) return "Entre na câmara do santuário";
    return "A memória de Avelora foi recuperada";
  }

  private handleInteraction(): void {
    if (this.paused) return;
    if (this.activeDialogue) {
      this.advanceDialogue();
      return;
    }
    const target = this.nearestInteractable();
    if (!target) return;
    if (target.id === "inscription") {
      this.progress.inscriptionRead = true;
      this.showDialogue("Inscrição", ["Quando o cristal despertar, atravesse a ponte que existia antes do Silêncio."]);
    } else if (target.id === "artifact") {
      if (!this.progress.inscriptionRead) return this.showNotice("A inscrição parece indicar o que fazer.");
      this.progress.artifactAwakened = true;
      this.showDialogue("O cristal", ["Uma luz azul percorre as ruínas.", "Pressione Q para alternar entre presente e passado."]);
    } else if (target.id === "memory") {
      if (!this.progress.artifactAwakened || this.progress.time !== "past") return this.showNotice("Um eco tênue aguarda no passado.");
      this.progress.memoryRead = true;
      this.showDialogue("Memória recuperada", ["Três símbolos guardam a câmara.", "A sequência é Sol, depois Lua e, por fim, Ondas."]);
    } else if (target.id === "sun" || target.id === "moon" || target.id === "wave") {
      const result = activateRune(this.progress, target.id);
      this.progress = result.progress;
      if (this.progress.puzzleSolved) this.doorBlocker.destroy();
      this.showNotice(result.message);
    } else if (target.id === "core") {
      if (!this.progress.puzzleSolved) return this.showNotice("A câmara permanece selada.");
      this.progress.endingReached = true;
      this.showDialogue("O último eco", ["A cidade perdida responde ao cristal.", "Além da floresta, outro santuário desperta."]);
    }
    this.refreshWorldVisuals();
    this.persist();
    this.updatePrompt();
  }

  private showDialogue(title: string, lines: string[]): void {
    this.activeDialogue = true;
    this.dialogueLines = lines;
    this.dialogueIndex = 0;
    this.dialogueBox.getByName<Phaser.GameObjects.Text>("dialogue-title")?.setText(title);
    this.dialogueBox.getByName<Phaser.GameObjects.Text>("dialogue-body")?.setText(lines[0] ?? "");
    this.dialogueBox.setVisible(true);
    this.prompt.setVisible(false);
    this.player.setVelocity(0, 0);
  }

  private advanceDialogue(): void {
    this.dialogueIndex += 1;
    if (this.dialogueIndex >= this.dialogueLines.length) {
      this.activeDialogue = false;
      this.dialogueBox.setVisible(false);
      this.persist();
      if (this.progress.endingReached) {
        this.paused = true;
        this.ui.endingScreen.hidden = false;
      }
      return;
    }
    this.dialogueBox.getByName<Phaser.GameObjects.Text>("dialogue-body")?.setText(this.dialogueLines[this.dialogueIndex]);
  }

  private toggleTime(): void {
    if (this.paused || !this.progress.artifactAwakened || this.activeDialogue) return;
    const next: TimeState = this.progress.time === "present" ? "past" : "present";
    if (next === "present" && this.player.y > 576 && this.player.y < 672 && this.player.x > 704 && this.player.x < 896) {
      this.showNotice("A ponte ainda não existe no presente. Volte para a margem.");
      return;
    }
    this.progress.time = next;
    this.syncWorldState();
    this.cameras.main.flash(260, next === "past" ? 74 : 164, next === "past" ? 190 : 177, 180);
    this.showNotice(next === "past" ? "O passado se revela." : "Você voltou ao presente.");
    this.persist();
  }

  private syncWorldState(): void {
    this.streamBlockers.forEach(blocker => blocker.destroy());
    this.streamBlockers = [];
    this.streamBlockers.push(this.addObstacle(0, 576, 704, 96));
    this.streamBlockers.push(this.addObstacle(896, 576, WORLD.width - 896, 96));
    if (this.progress.time === "present") this.streamBlockers.push(this.addObstacle(704, 576, 192, 96));
    if (this.progress.puzzleSolved && this.doorBlocker.active) this.doorBlocker.destroy();
    if (!this.progress.puzzleSolved && !this.doorBlocker.active) {
      this.doorBlocker = this.addObstacle(770, 344, 60, 40);
    }
    this.map.getLayer("Water")?.tilemapLayer?.setAlpha(this.progress.time === "past" ? 0.8 : 1);
    this.map.getLayer("Architecture")?.tilemapLayer?.setAlpha(this.progress.time === "past" ? 1 : 0.86);
    this.player?.setTint(this.progress.time === "past" ? 0xc5f4ec : 0xffffff);
    this.refreshWorldVisuals();
  }

  private refreshWorldVisuals(): void {
    RUNE_ORDER.forEach((id, index) => {
      this.runeSprites[id]?.setFrame(this.runeLit(index) ? `rune_${id}_on` : `rune_${id}`);
    });
    this.doorSeal?.setVisible(!this.progress.puzzleSolved);
    this.echoSprite?.setVisible(this.progress.time === "past" && !this.progress.memoryRead);
    const { artifact, core, inscription } = this.specialLights;
    if (artifact) artifact.strength = this.progress.artifactAwakened ? 1 : 0.45;
    if (core) core.strength = this.progress.puzzleSolved ? 1 : 0.55;
    if (inscription) inscription.strength = this.progress.inscriptionRead ? 0.25 : 0.55;
  }

  private showNotice(message: string): void {
    this.statusText.setText(message);
    this.noticeUntil = performance.now() + 2800;
    this.ui.status.textContent = message;
  }

  private persist(): void {
    if (this.player) {
      this.progress.x = Math.round(this.player.x);
      this.progress.y = Math.round(this.player.y);
    }
    try {
      saveProgress(this.progress);
      this.ui.continueButton.hidden = false;
    } catch (error) {
      console.error("Falha ao salvar o progresso V2.", error);
      this.ui.status.textContent = "Não foi possível salvar. O jogo continua, mas o progresso não foi gravado.";
    }
  }

  private startNew(): void {
    this.progress = newProgress(this.playerStart.x, this.playerStart.y);
    this.player.setPosition(this.playerStart.x, this.playerStart.y).setTint(0xffffff);
    this.paused = false;
    this.activeDialogue = false;
    this.ui.menu.hidden = true;
    this.ui.pauseScreen.hidden = true;
    this.ui.endingScreen.hidden = true;
    this.syncWorldState();
    this.updatePrompt();
    this.persist();
  }

  private continueGame(): void {
    const loaded = loadProgress();
    if (!loaded) {
      this.showNotice("O salvamento V2 é inválido. Iniciando uma nova jornada.");
      return this.startNew();
    }
    this.progress = loaded;
    this.player.setPosition(loaded.x, loaded.y);
    this.paused = false;
    this.ui.menu.hidden = true;
    this.syncWorldState();
    this.updatePrompt();
  }

  private resumeGame(): void {
    this.paused = false;
    this.ui.pauseScreen.hidden = true;
  }

  private pauseGame(): void {
    this.paused = true;
    this.player?.setVelocity(0, 0);
    this.ui.pauseScreen.hidden = false;
  }

  private cleanup(): void {
    this.game.events.off("game:new", this.startNew, this);
    this.game.events.off("game:continue", this.continueGame, this);
    this.game.events.off("game:resume", this.resumeGame, this);
    this.game.events.off("game:pause", this.pauseGame, this);
    this.events.off(Phaser.Scenes.Events.POST_UPDATE, this.followAndLight, this);
  }
}
