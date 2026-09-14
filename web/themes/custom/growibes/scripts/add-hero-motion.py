#!/usr/bin/env python3
"""Append context-specific hero motion CSS. No homepage orbit-dot."""

from pathlib import Path

ROOT = Path("/home/mukeysh/projects/gw/drupal/web/themes/custom/growibes/components/html/examples")
MARK = "/* gw-hero-motion */"

SHARED = """
@keyframes gw-spin{to{transform:rotate(360deg)}}
@keyframes gw-spin-rev{to{transform:rotate(-360deg)}}
@keyframes gw-spin-62{from{transform:rotate(62deg)}to{transform:rotate(422deg)}}
@keyframes gw-spin-neg18{from{transform:rotate(-18deg)}to{transform:rotate(342deg)}}
@keyframes gw-spin-neg22{from{transform:rotate(-22deg)}to{transform:rotate(338deg)}}
@keyframes gw-spin-34{from{transform:rotate(34deg)}to{transform:rotate(394deg)}}
@keyframes gw-spin-23{from{transform:rotate(23deg)}to{transform:rotate(383deg)}}
@keyframes gw-spin-neg31{from{transform:rotate(-31deg)}to{transform:rotate(329deg)}}
@keyframes gw-spin-center{from{transform:translate(-50%,-50%) rotate(0deg)}to{transform:translate(-50%,-50%) rotate(360deg)}}
@keyframes gw-spin-center-rev{from{transform:translate(-50%,-50%) rotate(0deg)}to{transform:translate(-50%,-50%) rotate(-360deg)}}
@keyframes gw-wso-r1{from{transform:translate(-50%,-50%) rotate(0deg)}to{transform:translate(-50%,-50%) rotate(360deg)}}
@keyframes gw-wso-r2{from{transform:translate(-50%,-50%) rotate(24deg) scaleY(.5)}to{transform:translate(-50%,-50%) rotate(384deg) scaleY(.5)}}
@keyframes gw-wso-r3{from{transform:translate(-50%,-50%) rotate(-20deg) scaleY(.38)}to{transform:translate(-50%,-50%) rotate(340deg) scaleY(.38)}}
@keyframes gw-wso-core{0%,100%{transform:translate(-50%,-50%) scale(1);opacity:1}50%{transform:translate(-50%,-50%) scale(1.08);opacity:.82}}
@keyframes gw-ai-ring{from{transform:rotate(35deg) scaleX(1.35)}to{transform:rotate(395deg) scaleX(1.35)}}
@keyframes gw-pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.28);opacity:.55}}
@keyframes gw-ping{0%{box-shadow:0 0 18px currentColor,0 0 0 0 currentColor}70%{box-shadow:0 0 18px currentColor,0 0 0 16px transparent}100%{box-shadow:0 0 18px currentColor,0 0 0 0 transparent}}
@keyframes gw-glow{0%,100%{filter:brightness(1)}50%{filter:brightness(1.22)}}
@keyframes gw-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes gw-dash{to{background-position:24px 0}}
@keyframes gw-dash-y{to{background-position:0 24px}}
@keyframes gw-sheen{from{background-position:100% 0}to{background-position:-100% 0}}
@keyframes gw-stroke{to{stroke-dashoffset:-96}}
@keyframes gw-wf{0%,10%{opacity:.38}16%,28%{opacity:1}36%,100%{opacity:.38}}
@keyframes gw-ring-out{0%{transform:scale(.55);opacity:.5}100%{transform:scale(1.45);opacity:0}}
@keyframes gw-breathe{0%,100%{opacity:.28}50%{opacity:.72}}
@keyframes gw-core-glow{0%,100%{box-shadow:0 0 24px rgba(216,255,89,.12)}50%{box-shadow:0 0 52px rgba(216,255,89,.38)}}
@keyframes gw-bar{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.62)}}
@keyframes gw-token-fill{0%,100%{transform:scaleX(.55)}50%{transform:scaleX(1)}}
@keyframes gw-border-glow{0%,100%{border-color:rgba(255,255,255,.13)}45%{border-color:rgba(202,255,77,.55)}}
@media (prefers-reduced-motion:reduce){
  .earth:before,.earth:after,.point,.lab1,.lab2,.lab3,.route,.box,.dcore,.globe:before,.globe:after,.orbit,.lang,.wfline,.wfnode,.arrow,.arrow2,.brain .o1,.brain .o2,.sat,.beam,.brain .core,.sphere,.sphere:after,.signal,.o1,.o2,.o3,.network path,.network .node,.orb:before,.orb:after,.core-ring,.core-ring:before,.core-ring:after,.orbit2,.core-word,.constellation line,.constellation circle,.pulse,.radar:after,.center,.network .line,.node,.ring,.world:after,.diagram:before,.diagram .core,.diagram .node,.funnel .f,.canvas .token,.canvas .component,.canvas .f-side,.mesh .link,.mesh .hub,.mesh .node,.ticks i,.clock .status,.clock .metric,.map .route,.map .node,.maplabel{animation:none!important}
}
"""

def layout(wrap: str, visual: str, col: str) -> str:
    return f"""
@media (max-width:1199px){{
  {visual}{{position:relative;right:auto;bottom:auto;margin:72px auto 0}}
}}
@media (min-width:1200px){{
  {wrap}{{display:grid;grid-template-columns:minmax(0,1fr) minmax(380px,{col});column-gap:clamp(48px,5.5vw,88px);align-items:center}}
  {visual}{{grid-column:2;grid-row:1/span 4;position:relative;right:auto;bottom:auto;width:100%;max-width:{col};justify-self:end;margin:0;align-self:center}}
  .hero h1{{max-width:none;font-size:clamp(56px,6.6vw,108px);line-height:.86}}
}}
"""


CSS = {
    "digital-platforms.css": layout(".in", ".globe", "460px") + """
.earth:before{animation:gw-spin 22s linear infinite}
.earth:after{animation:gw-spin-62 32s linear infinite}
.point{color:var(--lime);animation:gw-ping 2.4s ease-out infinite}
.p2{color:var(--cyan);animation-delay:.8s}
.p3{color:var(--orange);animation-delay:1.6s}
.lab1,.lab2,.lab3{animation:gw-float 5.4s ease-in-out infinite}
.lab2{animation-delay:.7s}
.lab3{animation-delay:1.4s}
""",
    "enterprise-drupal.css": """
.route{background-color:transparent;background-image:repeating-linear-gradient(90deg,#888 0 7px,transparent 7px 14px);background-size:14px 1px;background-repeat:repeat-x;animation:gw-dash 1.05s linear infinite}
.route.r2{animation-duration:1.35s;animation-direction:reverse}
.route.r3{right:auto;width:1px;background-image:repeating-linear-gradient(180deg,#888 0 7px,transparent 7px 14px);background-size:1px 14px;background-repeat:repeat-y;animation:gw-dash-y 1.7s linear infinite}
.dcore{animation:gw-glow 4s ease-in-out infinite}
.box{animation:gw-float 5s ease-in-out infinite}
.b2{animation-delay:.4s}
.b3{animation-delay:.8s}
.b4{animation-delay:1.2s}
.b5{animation-delay:1.6s}
.b6{animation-delay:2s}
""",
    "multilingual.css": """
.globe:before{animation:gw-spin 26s linear infinite}
.globe:after{animation:gw-spin 38s linear infinite reverse}
.orbit{background-image:repeating-linear-gradient(90deg,#d9ff3e 0 9px,transparent 9px 18px);background-size:18px 1px;border-top-color:transparent;height:1px;animation:gw-dash 1.25s linear infinite}
.lang{animation:gw-float 4.8s ease-in-out infinite}
.l2{animation-delay:.6s}
.l3{animation-delay:1.2s}
.l4{animation-delay:1.8s}
""",
    "content-governance.css": """
.wfline{background-color:transparent;background-image:repeating-linear-gradient(90deg,#ffffff55 0 8px,transparent 8px 16px);background-size:16px 100%;animation:gw-dash 1.4s linear infinite}
.wfline.b{animation-duration:1.85s;animation-direction:reverse}
.wfline.c{animation-duration:2.2s}
.wfnode{animation:gw-wf 5.6s ease-in-out infinite}
.n1{animation-delay:0s}
.n2{animation-delay:1.4s}
.n3{animation-delay:2.8s}
.n4{animation-delay:4.2s}
.arrow,.arrow2{background-image:repeating-linear-gradient(90deg,#d9ff3e 0 6px,transparent 6px 12px);background-size:12px 1px;border-top-color:transparent;height:1px;animation:gw-dash .85s linear infinite}
.arrow2{animation-direction:reverse}
""",
    "intelligent-enterprise.css": layout(".in", ".brain", "450px") + """
.brain .o1{animation:gw-spin 28s linear infinite}
.brain .o2{animation:gw-spin 18s linear infinite reverse}
.sat{animation:gw-float 4.6s ease-in-out infinite}
.s2{animation-delay:.5s}
.s3{animation-delay:1s}
.s4{animation-delay:1.5s}
.beam{background-image:linear-gradient(90deg,transparent 0%,rgba(105,233,255,.12) 38%,rgba(105,233,255,.95) 50%,rgba(105,233,255,.12) 62%,transparent 100%);background-size:220% 100%;animation:gw-sheen 1.8s linear infinite}
.b2{animation-duration:2.1s;animation-direction:reverse}
.b3{animation-duration:1.6s}
.b4{animation-duration:2.4s;animation-direction:reverse}
.brain .core{animation:gw-glow 3.2s ease-in-out infinite}
""",
    "drupal-ai.css": """
.sphere{animation:gw-glow 4.2s ease-in-out infinite}
.sphere:after{animation:gw-ai-ring 16s linear infinite}
.signal{animation:gw-float 5s ease-in-out infinite}
.s2{animation-delay:.5s}
.s3{animation-delay:1s}
.s4{animation-delay:1.5s}
.s5{animation-delay:2s}
.o1,.o2,.o3{border-style:dashed;animation:gw-breathe 3.6s ease-in-out infinite}
.o2{animation-delay:.8s}
.o3{animation-delay:1.6s}
""",
    "intelligent-enterprise-ai.css": """
.orb:before{animation:gw-spin-23 42s linear infinite}
.orb:after{animation:gw-spin-neg31 28s linear infinite}
.network path{stroke-dasharray:7 11;animation:gw-stroke 2.1s linear infinite}
.network path:nth-of-type(2){animation-duration:2.8s;animation-direction:reverse}
.network .node{color:var(--cyan);animation:gw-ping 2.5s ease-out infinite}
.n2{color:var(--gold);animation-delay:.3s}
.n3{color:var(--violet);animation-delay:.6s}
.n4{animation-delay:.9s}
.n5{color:var(--gold);animation-delay:1.2s}
.n6{color:var(--violet);animation-delay:1.5s}
""",
    "sovereign-core.css": """
.core-ring:before{border-style:dashed;animation:gw-spin 48s linear infinite}
.core-ring:after{border-style:dashed;animation:gw-spin 30s linear infinite reverse}
.orbit{animation:gw-spin-neg22 36s linear infinite reverse}
.orbit2{border-style:dashed;animation:gw-spin-34 52s linear infinite}
.core-word{animation:gw-breathe 6s ease-in-out infinite}
""",
    "connected-enterprise.css": """
.constellation line{stroke-dasharray:6 10;animation:gw-stroke 2.4s linear infinite}
.constellation line:nth-of-type(odd){animation-duration:3.1s;animation-direction:reverse}
.constellation circle:not(.pulse){animation:gw-pulse 2.4s ease-in-out infinite}
.constellation circle:nth-of-type(2){animation-delay:.4s}
.constellation circle:nth-of-type(3){animation-delay:.8s}
.constellation circle:nth-of-type(4){animation-delay:1.2s}
.constellation circle:nth-of-type(5){animation-delay:1.6s}
.constellation .pulse{transform-box:fill-box;transform-origin:center;animation:gw-ring-out 3.4s ease-out infinite}
""",
    "digital-trust.css": """
.radar:after{content:"";position:absolute;inset:8%;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 68%,rgba(255,90,78,.34) 82%,transparent 100%);animation:gw-spin 4.6s linear infinite;pointer-events:none;mix-blend-mode:screen}
.radar .pulse{color:var(--red);animation:gw-ping 2.2s ease-out infinite}
.p2{color:var(--blue);animation-delay:.7s}
.p3{animation-delay:1.4s}
.center{animation:gw-glow 3.6s ease-in-out infinite}
""",
    "cloud-devops.css": layout(".hero-in", ".network", "460px") + """
.network .line{background-image:linear-gradient(90deg,transparent 0%,rgba(110,231,255,.12) 38%,rgba(110,231,255,.95) 50%,rgba(110,231,255,.12) 62%,transparent 100%);background-size:220% 100%;animation:gw-sheen 1.6s linear infinite}
.l2,.l4{animation-direction:reverse;animation-duration:1.95s}
.l3{animation-duration:1.35s}
.l5{animation-duration:2.15s}
.network .node{animation:gw-float 4.4s ease-in-out infinite}
.n1{animation:gw-glow 3s ease-in-out infinite}
.n2{animation-delay:.3s}
.n3{animation-delay:.6s}
.n4{animation-delay:.9s}
.n5{animation-delay:1.2s}
""",
    "wso2.css": """
.ring{border-style:dashed;animation:gw-wso-r1 22s linear infinite}
.ring.r2{border-style:solid;animation:gw-wso-r2 14s linear infinite reverse}
.ring.r3{border-style:solid;animation:gw-wso-r3 26s linear infinite}
.orbit .core{animation:gw-wso-core 2.8s ease-in-out infinite}
""",
    "ibp.css": """
.point{color:var(--green);animation:gw-ping 2.1s ease-out infinite}
.p2{animation-delay:.45s}
.p3{animation-delay:.9s}
.p4{animation-delay:1.35s}
.world:after{animation:gw-spin-center 42s linear infinite}
""",
    "confidential-enterprise.css": """
.diagram:before{border-style:dashed;animation:gw-spin 40s linear infinite}
.diagram .core{animation:gw-core-glow 3.4s ease-in-out infinite}
.diagram .node{animation:gw-float 5.2s ease-in-out infinite}
.n2{animation-delay:.6s}
.n3{animation-delay:1.2s}
.n4{animation-delay:1.8s}
""",
    "marketing-automation.css": layout(".hero-in", ".funnel", "440px") + """
.funnel .f{animation:gw-border-glow 4.8s ease-in-out infinite,gw-float 5.6s ease-in-out infinite}
.f2{animation-delay:.6s,.6s}
.f3{animation-delay:1.2s,1.2s}
.f4{animation-delay:1.8s,1.8s}
""",
    "design-systems.css": layout(".hero-in", ".canvas", "470px") + """
.canvas .token{transform-origin:left center;animation:gw-token-fill 3.4s ease-in-out infinite}
.token.s{animation-duration:2.6s}
.canvas .component{animation:gw-glow 3.8s ease-in-out infinite}
.canvas .f-side{animation:gw-float 5.2s ease-in-out infinite}
.canvas .mini div{animation:gw-breathe 3.2s ease-in-out infinite}
.canvas .mini div:last-child{animation-delay:.8s}
""",
    "connected-apis.css": layout(".in", ".mesh", "480px") + """
.mesh .link{background-image:linear-gradient(90deg,transparent 0%,rgba(109,232,255,.12) 38%,rgba(109,232,255,.95) 50%,rgba(109,232,255,.12) 62%,transparent 100%);background-size:220% 100%;animation:gw-sheen 1.7s linear infinite}
.l2,.l4{animation-direction:reverse;animation-duration:2.1s}
.mesh .hub{animation:gw-glow 3.2s ease-in-out infinite}
.mesh .node{animation:gw-float 4.8s ease-in-out infinite}
.mesh .b{animation-delay:.4s}
.mesh .c{animation-delay:.8s}
.mesh .d{animation-delay:1.2s}
""",
    "continuous-engineering.css": layout(".in", ".clock", "420px") + """
.ticks i{transform-origin:center bottom;animation:gw-bar 2.2s ease-in-out infinite}
.ticks i:nth-child(2){animation-delay:.1s}
.ticks i:nth-child(3){animation-delay:.2s}
.ticks i:nth-child(4){animation-delay:.3s}
.ticks i:nth-child(5){animation-delay:.4s}
.ticks i:nth-child(6){animation-delay:.5s}
.ticks i:nth-child(7){animation-delay:.6s}
.ticks i:nth-child(8){animation-delay:.7s}
.ticks i:nth-child(9){animation-delay:.8s}
.ticks i:nth-child(10){animation-delay:.9s}
.clock .status{animation:gw-breathe 2.4s ease-in-out infinite}
.clock .metric{animation:gw-glow 4s ease-in-out infinite}
""",
    "strategy.css": layout(".in", ".map", "520px") + """
.map .route{background-size:220% 100%;animation:gw-sheen 2.6s linear infinite}
.map .node{color:#5267ff;animation:gw-ping 2.2s ease-out infinite}
.n2{color:#a9f7cf;animation-delay:.45s}
.n3{color:#f5c75d;animation-delay:.9s}
.n4{color:#ff5d52;animation-delay:1.35s}
.maplabel{animation:gw-float 5s ease-in-out infinite}
.m2{animation-delay:.4s}
.m3{animation-delay:.8s}
.m4{animation-delay:1.2s}
""",
}


def strip_old(css: str) -> str:
    if MARK in css:
        return css.split(MARK)[0].rstrip() + "\n"
    return css.rstrip() + "\n"


def main() -> None:
    for name, extra in CSS.items():
        path = ROOT / name
        css = strip_old(path.read_text())
        path.write_text(css + "\n" + MARK + extra + SHARED)
        print("css", name)


if __name__ == "__main__":
    main()
