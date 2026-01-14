/* huminlabs-forceRender.js — hard repaint fix */
(function() {
  const BG_HEX = 0xf4f1de;
  const BG_RGBA = [0.956, 0.945, 0.871, 1.0];

  function forceBackground() {
    const v = window.viewer || window.app?.viewer;
    const s = v?.sceneSetup;
    if (!s) return false;

    try {
      const r = s.renderer;
      const c = s.camera || s.pCamera;
      const scene = s.scene || s.rootGroup;

      if (r?.setClearColor) r.setClearColor(BG_HEX, 1);
      const gl = r?.getContext?.();
      if (gl?.clearColor) gl.clearColor(...BG_RGBA);

      if (scene && c && r?.render) {
        r.render(scene, c);  // ← force draw
        console.log("HUMIN CAD: Background rendered immediately.");
        return true;
      }
    } catch (e) {
      console.warn("HUMIN CAD: render kick failed", e);
    }
    return false;
  }

  let tries = 0;
  const watch = setInterval(() => {
    if (forceBackground() || ++tries > 100) clearInterval(watch);
  }, 200);
})();
