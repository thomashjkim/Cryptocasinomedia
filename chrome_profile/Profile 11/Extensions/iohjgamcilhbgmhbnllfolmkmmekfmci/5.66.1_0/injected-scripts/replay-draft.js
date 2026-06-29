export const ids=["378"];export const modules={65192:function(e,t,i){i.r(t),i.d(t,{Rewind:()=>$});var r=i(52322),n=i(7184),a=i(77938),o=i(22271),s=i(76524),l=i(63403),d=i(6891),c=i(70621),h=i(49710),u=i(75958),p=i(2784),w=i(94938),f=i(28128),m=i(61525),g=i(92487),v=i(20004);function y(e,t){let i=e.current?.querySelector("iframe");if(t){let e=i?.getBoundingClientRect();return{height:e?.height?e.height+"px":"100%",width:e?.width?e.width+"px":"100%"}}return{height:i?.scrollHeight?i.scrollHeight+"px":"100%",width:i?.scrollWidth?i.scrollWidth+"px":"100%"}}let x=e=>{let t=Number.parseFloat(e.width),i=Number.parseFloat(e.height);return isNaN(t)||isNaN(i)||0===i?16/9:t/i},j=e=>{let t=e.iframe.contentDocument;if(t)for(let e of Array.from(t.querySelectorAll("audio")))e?.pause()},b=e=>{let{events:t,initializeStoreWithReplayer:i}=e,n=(0,p.useRef)(null),a=(0,p.useRef)(null),[o,s]=(0,p.useState)(null),[l,d]=(0,p.useState)(y(a)),c=(0,p.useCallback)(e=>{!function(e,t){e.style.position="absolute",e.style.left="50%",e.style.top="50%";let i=t?{width:window.innerWidth,height:window.innerHeight}:{width:e.parentElement?.clientWidth??window.innerWidth,height:e.parentElement?.clientHeight??window.innerHeight},r={width:e.scrollWidth,height:e.scrollHeight},n=function(e,t){let i=e.height/t.height;return Math.min(e.width/t.width,i)}(t?{width:window.innerWidth,height:window.innerHeight}:i,r);e.style.transform=`scale(${n}) translate(-50%, -50%)`}(e.wrapper,!1),d(y(a))},[]);(0,p.useEffect)(()=>{if(!a.current)return;a.current.childNodes.forEach(e=>e.remove());let e=new w.xB(t,{UNSAFE_replayCanvas:!0,speed:1,root:a.current,unpackFn:void 0,mouseTail:!1,skipInactive:!1,triggerFocus:!1,showDebug:!1,showWarning:!1});if(s(e),e)return j(e),e.iframe.setAttribute("sandbox",""),()=>e.pause()},[t]),(0,p.useEffect)(()=>{if(!o||!n.current)return;let e=new ResizeObserver(()=>{requestAnimationFrame(()=>{c(o)})});return e.observe(n.current),()=>e.disconnect()},[o,c]),(0,p.useEffect)(()=>{i?.(o??void 0)},[o,i]);let h=x(l);return(0,r.jsx)(R,{ref:n,$aspectRatio:h,children:(0,r.jsx)(S,{children:(0,r.jsx)(E,{ref:a,className:"rr-block session-player"})})})},S=n.Z.div`
  width: 100%;
  height: 100%;
`,R=n.Z.div`
  position: relative;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  margin-bottom: 16px;
  outline: none;
  user-select: none;
  overflow: hidden;
  aspect-ratio: ${e=>e.$aspectRatio};
`,E=n.Z.div`
  position: relative;
  width: 100%;
  height: 100%;

  // rounded corners for the iframe wrapper
  > div:first-child {
    border-radius: 12px;
    -webkit-mask: linear-gradient(white, white);
    mask: linear-gradient(white, white);
  }

  iframe {
    background: var(--white);
  }
`;function k(e){let{status:t,loading:i,...n}=e,a=n.events;return"Uploading"===t?(0,r.jsx)(F,{children:(0,r.jsx)(N,{children:"Uploading your session..."})}):"Failed"===t?(0,r.jsx)(F,{children:(0,r.jsx)(N,{children:"Failed to upload your session..."})}):i?(0,r.jsx)(F,{children:(0,r.jsx)(N,{children:"Loading your session..."})}):a.length<2?(0,r.jsx)(F,{children:(0,r.jsx)(N,{children:"There is nothing to play \uD83D\uDE33 "})}):(0,r.jsx)(A,{children:(0,r.jsx)(b,{...n})})}let A=n.Z.div`
  position: relative;
  min-width: 100%;
  min-height: 100%;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`,F=n.Z.div`
  position: relative;
  display: flex;
  align-items: center;
  align-self: center;
  justify-content: center;
  width: 100%;
  height: 100%;
`,N=n.Z.div`
  text-align: center;
  font-size: 16px;
  color: #333;
`;var T=i(37079);let Z=(0,u.Pi)(function(e){let t=e.captureDataStore.rewind.replayEvents??[],i=(0,v.k)(g.K8O.Replay);return(0,r.jsxs)(H,{children:[(0,r.jsx)(C,{children:(0,r.jsx)(k,{events:t,loading:!e.captureDataStore.rewind.replayEvents,initializeStoreWithReplayer:t=>t&&e.videoTrimStore.initializePlaybackForSessionReplay(t,i())})}),e.errorComponent??null,(0,r.jsx)(T.u,{videoTrimStore:e.videoTrimStore,isRewind:!0})]})}),H=n.Z.div`
  display: flex;
  flex-direction: column;
  height: 80vh;

  ${m.w.tabletLandscape} {
    min-width: unset;
    min-height: unset;
  }
  ${m.w.tablet} {
    width: 100%;
    align-items: unset;
    height: 400px;
  }
`,C=n.Z.div`
  display: flex;
  flex-grow: 1;
  min-width: 0;
  min-height: 0;
`;var D=i(76502),W=i(16140),z=i(82608),U=i(25171);let $=(0,u.Pi)(function(e){let t=(0,f.z3)(),i=(0,f.dR)(),n=i.capture,u=n.type===h.K8.Replay&&("draft"===n.state.name||"pre_draft"===n.state.name)&&n.state.payload.atTabId===t,m=(0,p.useRef)(!1),g=(0,f.EO)(),v=(0,f.MU)(),y=function(e,t){let[i,r]=(0,p.useState)(null),n=(0,f.MU)(),a=(0,p.useRef)(!1);return(0,p.useEffect)(()=>{let i=async()=>{let t;try{t=await n.send({eventName:"GenerateRewind",dest:{component:l.wA.Main,location:void 0},data:{events:"all"},timeout:z.eq("30s")})}catch(e){c.k.error("unexpected error generating rewind",{error:e}),await n.send({eventName:"Dismiss",dest:{component:l.wA.Main,location:void 0},data:{storeDraft:!0}});return}let{events:i,fullscreenDataUrl:a}=t,o=Array.isArray(i)?i:[];e.rewind.setReplayEvents(o),e.rewind.setFullscreenDataUrl(a),r({events:o,fullscreenDataUrl:a})};return!a.current&&t&&(0,U.Y)().span("instant_replay_capture","get-events",i),()=>{a.current=!0}},[e.rewind,n,t]),i}(g,u),x=y?.events??[],j=(0,a.XE)(x),b=a.lh(x)?.filter(e=>e.error),S=y?.events.some(e=>e.type===w.tw.FullSnapshot);(0,p.useEffect)(()=>{m.current||"boolean"!=typeof S||c.k.info("replay draft render",{success:S}),m.current=!0},[S]);let R=!!S&&!i.isResumedDraft();return((0,d.Q)({interaction:"instant_replay_capture",variant:"success",policy:{when:"onCondition",condition:R}}),y)?(0,r.jsx)(D.Z,{onSubmit:e=>(v.send({eventName:"FreezeClickEvents",dest:{component:l.wA.HostScript,location:l.Ye.HostScripts.AdditionalHooks,tabId:t},data:!1}),(0,W.Z)({broker:v,data:e,captureType:h.K8.Replay})),children:S?(0,r.jsx)(Z,{videoTrimStore:e.videoTrimStore,captureDataStore:g,errorComponent:(0,r.jsx)(_,{children:(0,r.jsx)(o.h,{inTrimmingContext:!0,consoleErrors:j,networkErrors:b,videoAnnotationEvents:void 0,startTimestamp:(0,a.Cy)(x)??0,duration:e.videoTrimStore.playback.duration})})}):(0,r.jsx)(s.d,{title:"Instant replay error",body:"Sorry we weren't able to capture an instant replay. Please try again after refreshing the page you wish to capture."})}):null}),_=n.Z.div`
  padding-left: 72px;
  padding-right: 24px;
`}};
//# sourceMappingURL=replay-draft.js.map