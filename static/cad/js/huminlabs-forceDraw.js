/* huminlabs-forceDraw.js — trigger first render cycle manually */
(function() {
  const BG_HEX = 0xf4f1de;
  const BG_RGBA = [0.956, 0.945, 0.871, 1.0];

  function forceInitialRender() {
    const v = window.viewer || window.app?.viewer;
    const s = v?.sceneSetup;
    if (!s || !s.renderer) return false;

    try {
      const r = s.renderer;
      const gl = r.getContext?.();

      // Apply HUMIN beige immediately
      r.setClearColor(BG_HEX, 1);
      if (gl?.clearColor) gl.clearColor(...BG_RGBA);

      // 🔥 Critical: trigger JSketcher’s own render once
      s.requestRender?.();

      console.log("✅ HUMIN CAD: Triggered initial render with beige background.");
      return true;
    } catch (e) {
      console.warn("⚠️ HUMIN CAD: forceInitialRender failed:", e);
      return false;
    }
  }

  function waitForViewer() {
    const ready = window.viewer?.sceneSetup?.renderer;
    if (ready) {
      // Wait one animation frame so the renderer has dimensions
      requestAnimationFrame(() => {
        forceInitialRender();
      });
    } else {
      requestAnimationFrame(waitForViewer);
    }
  }

  window.addEventListener("load", waitForViewer);
})();
