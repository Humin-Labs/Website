// Simple interactive 4-bar linkage simulator
(function () {
  const TAU = Math.PI * 2;

  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }

  function solveFourBar(a, b, c, d, theta) {
    // numeric solve for output angle
    let phi = theta * 0.6;
    for (let i = 0; i < 40; i++) {
      const Ax=0, Ay=0, Bx=b*Math.cos(theta), By=b*Math.sin(theta);
      const Dx=a, Dy=0;
      const Cx=Dx+d*Math.cos(phi), Cy=Dy+d*Math.sin(phi);
      const rx=Cx-Bx, ry=Cy-By;
      const f=Math.sqrt(rx*rx+ry*ry)-c;
      const Cxp=-d*Math.sin(phi), Cyp=d*Math.cos(phi);
      const dist=Math.max(1e-6,Math.sqrt(rx*rx+ry*ry));
      const df=(Cxp*rx+Cyp*ry)/dist;
      phi-=clamp(f/Math.max(1e-6,df),-0.25,0.25);
    }
    return ((phi%TAU)+TAU)%TAU;
  }

  function effortLevel(theta, phi){
    const deadIn = Math.abs(Math.sin(theta)) < 0.15 ? 1 : 0;
    const deadOut = Math.abs(Math.sin(phi)) < 0.15 ? 1 : 0;
    return ["Low","Medium","High"][clamp(deadIn+deadOut,0,2)];
  }

  function mount(root){
    const a = +root.dataset.ground || 180;
    const b = +root.dataset.input  || 70;
    const c = +root.dataset.coupler|| 140;
    const d = +root.dataset.output || 120;
    let theta = (+root.dataset.theta0 || 0) * Math.PI/180;

    const svg = root.querySelector("svg");
    const handle = svg.querySelector("#handle");
    const readIn = root.querySelector("[data-read=in]");
    const readOut = root.querySelector("[data-read=out]");
    const readEff = root.querySelector("[data-read=eff]");

    function draw(){
      const phi = solveFourBar(a,b,c,d,theta);
      const Ax=0,Ay=0, Bx=b*Math.cos(theta), By=b*Math.sin(theta);
      const Dx=a,Dy=0;
      const Cx=Dx+d*Math.cos(phi), Cy=Dy+d*Math.sin(phi);

      svg.querySelector("#ground").setAttribute("d",`M ${Ax},${Ay} L ${Dx},${Dy}`);
      svg.querySelector("#linkA").setAttribute("d",`M ${Ax},${Ay} L ${Bx},${By}`);
      svg.querySelector("#linkB").setAttribute("d",`M ${Bx},${By} L ${Cx},${Cy}`);
      svg.querySelector("#linkC").setAttribute("d",`M ${Cx},${Cy} L ${Dx},${Dy}`);

      handle.setAttribute("cx",Bx);
      handle.setAttribute("cy",By);

      if (readIn)  readIn.textContent  = (theta*180/Math.PI).toFixed(1)+"°";
      if (readOut) readOut.textContent = (phi*180/Math.PI).toFixed(1)+"°";
      if (readEff) readEff.textContent = effortLevel(theta,phi);

      if (root._update) root._update(theta,phi);
    }

    // --- pointer drag control ---
    function onDrag(evt){
      const pt = svg.createSVGPoint();
      pt.x = evt.clientX; pt.y = evt.clientY;
      const ctm = svg.getScreenCTM().inverse();
      const p = pt.matrixTransform(ctm);
      theta = Math.atan2(p.y, p.x);
      draw();
    }

    handle.addEventListener("pointerdown", (evt)=>{
      evt.preventDefault();
      svg.addEventListener("pointermove", onDrag);
      svg.setPointerCapture(evt.pointerId);
    });

    svg.addEventListener("pointerup", (evt)=>{
      svg.removeEventListener("pointermove", onDrag);
      svg.releasePointerCapture(evt.pointerId);
    });

    draw();
  }

  // expose + autorun
  window.mountLinkages = function(){
    document.querySelectorAll(".linkage-4bar").forEach(mount);
  };
  document.addEventListener("DOMContentLoaded", window.mountLinkages);
})();
