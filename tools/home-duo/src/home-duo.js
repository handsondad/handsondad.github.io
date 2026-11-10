// 小念和爸爸站在小星球上。角色装配、卡通着色、描边和星球场景移植自 Bodyverse 首页
// （bodyverse/src/components/run-lab/{rig.ts,world.tsx} 与 RunLab3D.tsx），去掉了跑步实验和透视器官。
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { clone as cloneSkinned } from "three/examples/jsm/utils/SkeletonUtils.js";

const looks = {
  nian: {
    palette: { Skin: "#f5c9a6", Shirt: "#ff8a5c", Pants: "#3d6fd6", Belt: "#2b3f80", Face: "#3a2418", Hair: "#5a3a22" },
    height: 1.3, headScale: 1, glasses: false, x: 0.5, facing: -0.25
  },
  dad: {
    palette: { Skin: "#eab892", Shirt: "#3f78c9", Pants: "#4a4d5c", Belt: "#2a2c36", Face: "#2e1d14", Hair: "#2a1c14" },
    height: 1.85, headScale: 0.8, glasses: true, x: -0.6, facing: 0.55
  }
};

const planetRadius = 5;
const runFacing = 0.9;
// Raises the framing so the characters sit lower, leaving room for speech bubbles above their heads.
const lift = 0.35;
const up = new THREE.Vector3(0, 1, 0);
const runDirection = new THREE.Vector3(Math.sin(runFacing), 0, Math.cos(runFacing));
const spinAxis = new THREE.Vector3().crossVectors(up, runDirection).normalize();
const lookTarget = new THREE.Vector3(0, 0.95 + lift, 0);
const damp = (from, to, rate, dt) => to + (from - to) * Math.exp(-rate * dt);

let gradient = null;
function toonGradient() {
  const tones = new Uint8Array([90, 90, 90, 255, 170, 170, 170, 255, 255, 255, 255, 255]);
  const texture = new THREE.DataTexture(tones, 3, 1, THREE.RGBAFormat);
  texture.minFilter = THREE.NearestFilter;
  texture.magFilter = THREE.NearestFilter;
  texture.needsUpdate = true;
  return texture;
}
const toon = (color) => new THREE.MeshToonMaterial({ color, gradientMap: (gradient ??= toonGradient()) });

// Screen-space inverted hull: constant-width cartoon outline that follows skinning.
function outlineMaterial() {
  const material = new THREE.MeshBasicMaterial({ color: "#3b2618", side: THREE.BackSide });
  material.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader.replace("#include <project_vertex>", `#include <project_vertex>
      vec2 outlineDir = normalize((projectionMatrix * vec4(transformedNormal, 0.0)).xy + 1e-5);
      gl_Position.xy += outlineDir * 0.007 * gl_Position.w;`);
  };
  return material;
}

// The Face mesh holds the eyes (lower part) and eyebrows (top), so its box frames where the lenses go.
function addGlasses(head, face) {
  const width = face.max.x - face.min.x;
  const ring = width * 0.18;
  const y = face.min.y + (face.max.y - face.min.y) * 0.35;
  const z = face.max.z + ring * 0.2;
  const frame = toon("#24242c");
  const glasses = new THREE.Group();
  for (const side of [1, -1]) {
    const lens = new THREE.Mesh(new THREE.TorusGeometry(ring, ring * 0.16, 8, 28), frame);
    lens.position.set(side * width * 0.3, y, z);
    glasses.add(lens);
  }
  const bridge = new THREE.Mesh(new THREE.CylinderGeometry(ring * 0.12, ring * 0.12, width * 0.6 - ring * 2, 6), frame);
  bridge.rotation.z = Math.PI / 2;
  bridge.position.set(0, y + ring * 0.2, z);
  glasses.add(bridge);
  head.attach(glasses);
}

function buildRig(gltf, look) {
  const model = cloneSkinned(gltf.scene);
  const root = new THREE.Group();
  root.add(model);
  const meshes = [];
  model.traverse((object) => {
    if (object.isSkinnedMesh) meshes.push(object);
  });

  const outline = outlineMaterial();
  const skinMats = [];
  let faceMat = null;
  let skinMesh = null;
  let faceMesh = null;
  for (const mesh of meshes) {
    const name = mesh.material.name;
    const material = toon(look.palette[name] ?? "#cccccc");
    mesh.material = material;
    mesh.frustumCulled = false;
    if (name === "Skin") {
      skinMats.push(material);
      skinMesh = mesh;
    }
    if (name === "Face") {
      faceMat = material;
      faceMesh = mesh;
    }
    const hull = mesh.clone();
    hull.material = outline;
    mesh.parent?.add(hull);
  }

  const mixer = new THREE.AnimationMixer(model);
  const actions = {};
  for (const clip of gltf.animations) actions[clip.name] = mixer.clipAction(clip);
  actions.Idle.play();
  mixer.update(0);
  model.getObjectByName("Head")?.scale.setScalar(look.headScale);
  model.updateMatrixWorld(true);
  for (const mesh of meshes) mesh.skeleton.update();
  const rawBox = new THREE.Box3().setFromObject(model);
  const scale = look.height / (rawBox.max.y - rawBox.min.y);
  model.scale.setScalar(scale);
  model.position.y = -rawBox.min.y * scale;
  root.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(model);

  const bone = (name) => {
    const found = model.getObjectByName(name);
    if (!found) throw new Error(`角色骨骼缺失：${name}`);
    return found;
  };
  const head = bone("Head");
  const neck = bone("Neck");
  const headPos = head.getWorldPosition(new THREE.Vector3());
  const headH = box.max.y - headPos.y;
  const headCenter = headPos.clone().addScaledVector(up, headH * 0.5);

  // Blush on both cheeks, glued to the head bone.
  const ray = new THREE.Raycaster();
  const cheekMat = new THREE.MeshBasicMaterial({ color: "#ff6f86", transparent: true, opacity: 0.2, depthWrite: false });
  for (const side of [1, -1]) {
    const y = headPos.y + headH * 0.3;
    const x = side * headH * 0.3;
    ray.set(new THREE.Vector3(x, y, box.max.z + 1), new THREE.Vector3(0, 0, -1));
    const point = ray.intersectObjects(skinMesh ? [skinMesh] : meshes, false)[0]?.point
      ?? new THREE.Vector3(x, y, headCenter.z + headH * 0.45);
    const out = point.clone().sub(headCenter).normalize();
    const cheek = new THREE.Mesh(new THREE.CircleGeometry(headH * 0.085, 24), cheekMat);
    cheek.scale.set(1.25, 0.8, 1);
    cheek.position.copy(point).addScaledVector(out, headH * 0.012);
    cheek.lookAt(point.clone().addScaledVector(out, 1));
    cheek.renderOrder = 2;
    head.attach(cheek);
  }
  if (look.glasses && faceMesh) addGlasses(head, new THREE.Box3().setFromObject(faceMesh));

  root.position.set(look.x, 0.05, 0);
  root.rotation.y = look.facing;
  return {
    root, mixer, actions, oneShot: null, head, neck, facing: look.facing,
    skinColor: skinMats[0]?.color.clone() ?? new THREE.Color(), faceMat, faceBase: faceMat?.color.clone() ?? new THREE.Color(),
    nextBlink: 2 + Math.random() * 2, gaze: new THREE.Vector2(),
    // three's mixer skips bones whose value didn't change, so gaze offsets must be undone manually.
    headPose: head.quaternion.clone(), neckPose: neck.quaternion.clone(), headScale: look.headScale
  };
}

function playOnce(rig, clipName) {
  const action = rig.actions[clipName];
  if (!action) return;
  rig.oneShot?.fadeOut(0.1);
  action.reset().setLoop(THREE.LoopOnce, 1).fadeIn(0.15).play();
  action.clampWhenFinished = true;
  rig.actions.Idle.fadeOut(0.15);
  rig.oneShot = action;
}

function seeded(seed) {
  let value = seed;
  return () => {
    value = (value * 16807) % 2147483647;
    return (value - 1) / 2147483646;
  };
}

function onSurface(object, angle, side, height = 0) {
  const normal = up.clone().multiplyScalar(Math.cos(angle)).addScaledVector(runDirection, Math.sin(angle)).addScaledVector(spinAxis, side).normalize();
  object.position.copy(normal).multiplyScalar(planetRadius + height);
  object.quaternion.setFromUnitVectors(up, normal);
  return object;
}

function buildPlanet() {
  const random = seeded(7);
  const planet = new THREE.Group();
  planet.add(new THREE.Mesh(new THREE.SphereGeometry(planetRadius, 64, 40), toon("#8ed46b")));
  const path = new THREE.Mesh(new THREE.TorusGeometry(planetRadius - 0.94, 1, 10, 160), toon("#f6dca4"));
  path.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), spinAxis);
  planet.add(path);

  const trunkMat = toon("#a8714a");
  const leafMats = ["#4fb35a", "#6cc56a", "#3f9e57"].map(toon);
  const flowerMats = ["#ff7aa2", "#ffd23f", "#ffffff", "#b38cff"].map(toon);
  const capMat = toon("#ff5a4f");
  const dotMat = toon("#fff7ec");
  const stemMat = toon("#fff0d6");
  const pebbleMat = toon("#d9c08a");

  for (let i = 0; i < 16; i += 1) {
    const tree = new THREE.Group();
    const height = 0.45 + random() * 0.35;
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.1, height, 8), trunkMat);
    trunk.position.y = height / 2;
    tree.add(trunk);
    const leaves = leafMats[i % leafMats.length];
    if (random() > 0.4) {
      const crown = new THREE.Mesh(new THREE.IcosahedronGeometry(0.38 + random() * 0.18, 1), leaves);
      crown.position.y = height + 0.25;
      tree.add(crown);
    } else {
      for (let k = 0; k < 3; k += 1) {
        const cone = new THREE.Mesh(new THREE.ConeGeometry(0.42 - k * 0.1, 0.5, 9), leaves);
        cone.position.y = height + 0.1 + k * 0.28;
        tree.add(cone);
      }
    }
    tree.scale.setScalar(0.9 + random() * 0.6);
    planet.add(onSurface(tree, (i / 16) * Math.PI * 2 + random() * 0.2, 0.32 + random() * 0.5));
  }

  for (let i = 0; i < 7; i += 1) {
    const mushroom = new THREE.Group();
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 0.16, 8), stemMat);
    stem.position.y = 0.08;
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.14, 14, 10, 0, Math.PI * 2, 0, Math.PI / 2), capMat);
    cap.position.y = 0.15;
    mushroom.add(stem, cap);
    for (let k = 0; k < 3; k += 1) {
      const dot = new THREE.Mesh(new THREE.SphereGeometry(0.025, 6, 6), dotMat);
      const a = (k / 3) * Math.PI * 2;
      dot.position.set(Math.cos(a) * 0.08, 0.26, Math.sin(a) * 0.08);
      mushroom.add(dot);
    }
    planet.add(onSurface(mushroom, random() * Math.PI * 2, (random() > 0.5 ? 1 : -1) * (0.2 + random() * 0.15)));
  }

  for (let i = 0; i < 36; i += 1) {
    const flower = new THREE.Group();
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.14, 4), leafMats[0]);
    stem.position.y = 0.07;
    const bloom = new THREE.Mesh(new THREE.IcosahedronGeometry(0.05, 0), flowerMats[i % flowerMats.length]);
    bloom.position.y = 0.15;
    flower.add(stem, bloom);
    const side = (random() > 0.45 ? 1 : -1) * (0.13 + random() * 0.5);
    planet.add(onSurface(flower, random() * Math.PI * 2, side));
  }

  for (let i = 0; i < 18; i += 1) {
    const pebble = new THREE.Mesh(new THREE.DodecahedronGeometry(0.05 + random() * 0.04, 0), pebbleMat);
    pebble.scale.y = 0.45;
    planet.add(onSurface(pebble, random() * Math.PI * 2, (random() - 0.5) * 0.12, 0.04));
  }
  planet.position.y = -planetRadius;
  return planet;
}

function buildCloud(random) {
  const cloud = new THREE.Group();
  const material = toon("#ffffff");
  for (let i = 0; i < 4; i += 1) {
    const puff = new THREE.Mesh(new THREE.SphereGeometry(0.45 + random() * 0.3, 16, 12), material);
    puff.position.set(i * 0.55 - 0.8, (i % 2) * 0.2, random() * 0.2);
    cloud.add(puff);
  }
  return cloud;
}

function disc(radius, color, position, extra = {}) {
  const mesh = new THREE.Mesh(new THREE.CircleGeometry(radius, 40), new THREE.MeshBasicMaterial({ color, ...extra }));
  mesh.position.set(...position);
  return mesh;
}

export async function mountDuo(stage, { modelUrl, reducedMotion }) {
  const gltf = await new GLTFLoader().loadAsync(modelUrl);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.domElement.className = "duo-canvas";
  renderer.domElement.setAttribute("aria-hidden", "true");
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 60);
  camera.position.set(0.6, 1.5 + lift, 6.2);

  scene.add(new THREE.HemisphereLight("#ffffff", "#ffd9b0", 1.6));
  const sun = new THREE.DirectionalLight("#ffffff", 2.1);
  sun.position.set(3, 6, 5);
  scene.add(sun, buildPlanet());
  const random = seeded(11);
  const clouds = [[-5, 3.6, -9], [1, 4.4, -11], [6, 3.2, -10], [-1.5, 2.6, -8]].map(([x, y, z]) => {
    const cloud = buildCloud(random);
    cloud.position.set(x, y, z);
    scene.add(cloud);
    return cloud;
  });
  scene.add(disc(1.1, "#ffe27a", [-4.5, 4.6, -14]));
  scene.add(disc(1.6, "#fff3c4", [-4.5, 4.6, -14.1], { transparent: true, opacity: 0.6 }));
  for (const look of Object.values(looks)) {
    const shadow = disc(look.height * 0.25, "#2f5a1f", [look.x, 0.07, 0], { transparent: true, opacity: 0.22, depthWrite: false });
    shadow.rotation.x = -Math.PI / 2;
    scene.add(shadow);
  }

  const rigs = Object.values(looks).map((look) => buildRig(gltf, look));
  for (const rig of rigs) {
    scene.add(rig.root);
    rig.mixer.addEventListener("finished", (event) => {
      if (event.action !== rig.oneShot) return;
      rig.oneShot.fadeOut(0.3);
      rig.oneShot = null;
      rig.actions.Idle.reset().fadeIn(0.3).play();
    });
  }

  let cue = 0;
  stage.addEventListener("duo:talk", () => {
    const clip = cue % 2 ? "Victory" : "Jump";
    cue += 1;
    for (const rig of rigs) playOnce(rig, clip);
  });

  const pointer = new THREE.Vector2();
  const raycaster = new THREE.Raycaster();
  const toPointer = (event) => {
    const rect = renderer.domElement.getBoundingClientRect();
    pointer.set(((event.clientX - rect.left) / rect.width) * 2 - 1, -((event.clientY - rect.top) / rect.height) * 2 + 1);
  };
  const hitCharacter = () => {
    raycaster.setFromCamera(pointer, camera);
    return raycaster.intersectObjects(rigs.map((rig) => rig.root), true).length > 0;
  };
  stage.addEventListener("pointermove", (event) => {
    toPointer(event);
    renderer.domElement.style.cursor = hitCharacter() ? "pointer" : "";
  });
  stage.addEventListener("pointerleave", () => pointer.set(0, 0));
  renderer.domElement.addEventListener("click", (event) => {
    toPointer(event);
    if (hitCharacter()) stage.dispatchEvent(new CustomEvent("duo:tap"));
  });

  const resize = () => {
    const { clientWidth: width, clientHeight: height } = stage;
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(stage);
  resize();

  const clock = new THREE.Clock();
  let visible = true;
  const frame = () => {
    const dt = Math.min(clock.getDelta(), 0.1);
    const time = clock.elapsedTime;
    const px = reducedMotion ? 0 : pointer.x;
    const py = reducedMotion ? 0 : pointer.y;

    const portrait = stage.clientWidth < stage.clientHeight * 0.95;
    camera.position.set(
      damp(camera.position.x, 0.6 + px * 0.3, 3, dt),
      damp(camera.position.y, 1.5 + lift + py * 0.15 + (portrait ? 0.25 : 0), 3, dt),
      portrait ? 7.3 : 6.2
    );
    camera.lookAt(lookTarget);

    for (const rig of rigs) {
      rig.actions.Idle.timeScale = reducedMotion ? 0.7 : 1;
      rig.head.quaternion.copy(rig.headPose);
      rig.neck.quaternion.copy(rig.neckPose);
      rig.mixer.update(dt);
      rig.head.scale.setScalar(rig.headScale);
      rig.headPose.copy(rig.head.quaternion);
      rig.neckPose.copy(rig.neck.quaternion);
      rig.gaze.x = damp(rig.gaze.x, THREE.MathUtils.clamp(0.1 - rig.facing + px * 0.6, -0.75, 0.75), 6, dt);
      // Never tilt down: a lowered head hides the face.
      rig.gaze.y = damp(rig.gaze.y, THREE.MathUtils.clamp(py * 0.15 + 0.12, 0, 0.3), 6, dt);
      rig.neck.rotateY(rig.gaze.x * 0.35);
      rig.head.rotateY(rig.gaze.x * 0.65);
      rig.head.rotateX(-rig.gaze.y);
      if (time > rig.nextBlink + 0.12) rig.nextBlink = time + 2 + Math.random() * 3;
      rig.faceMat?.color.copy(time > rig.nextBlink ? rig.skinColor : rig.faceBase);
    }
    if (!reducedMotion) {
      for (const cloud of clouds) {
        cloud.position.x -= dt * 0.08;
        if (cloud.position.x < -9) cloud.position.x = 9;
      }
    }
    renderer.render(scene, camera);
  };
  const sync = () => renderer.setAnimationLoop(visible && !document.hidden ? frame : null);
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    clock.getDelta();
    sync();
  }).observe(stage);
  document.addEventListener("visibilitychange", () => {
    clock.getDelta();
    sync();
  });

  stage.prepend(renderer.domElement);
  frame();
  sync();
  stage.classList.add("is-3d");
}
