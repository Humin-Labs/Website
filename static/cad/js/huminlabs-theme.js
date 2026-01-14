/* huminlabs-theme.js — HUMIN beige with delayed auto-render kick */
(function() {
  const BG_HEX = 0xf4f1de;
  const BG_RGBA = [0.956, 0.945, 0.871, 1.0];

  function applyTheme() {
    try {
      const viewer = window.viewer || window.app?.viewer;
      const scene = viewer?.scene;
      const renderer = viewer?.renderer;
      const gl = renderer?.getContext?.() || viewer?.gl;

      if (scene?.background?.setHex) scene.background.setHex(BG_HEX);
      if (renderer?.setClearColor) renderer.setClearColor(BG_HEX, 1);
      if (gl?.clearColor) gl.clearColor(...BG_RGBA);

      return viewer;
    } catch {
      return null;
    }
  }

  function forceRender(viewer) {
    try {
      const ctrl = viewer?.sceneSetup?.trackballControls || viewer?.controls;
      if (ctrl?.zoomStep) {
        ctrl.zoomStep(1, -1);
        ctrl.zoomStep(1, 1);
      } else {
        viewer?.requestRender?.();
      }
    } catch (e) {
      console.warn("HUMIN CAD: auto render trigger failed", e);
    }
  }

  // --- Watch for viewer creation ---
  let tries = 0;
  const watcher = setInterval(() => {
    const v = applyTheme();
    if (v || ++tries > 120) {
      clearInterval(watcher);
      if (v) {
        // Wait a bit longer so trackballControls definitely exist
        setTimeout(() => {
          applyTheme();
          forceRender(v);
        }, 1200);

        // Extra redundancy repaint after 3s (covers async loads)
        setTimeout(() => {
          applyTheme();
          forceRender(v);
        }, 3000);
      }
    }
  }, 250);

  // Maintain background periodically
  setInterval(applyTheme, 4000);

  // CSS fallback tint
  const style = document.createElement("style");
  style.textContent = `
    canvas, #viewer-container, #app canvas {
      background-color: #f4f1de !important;
      transition: background-color 0.3s ease;
    }`;
  document.head.appendChild(style);
})();
