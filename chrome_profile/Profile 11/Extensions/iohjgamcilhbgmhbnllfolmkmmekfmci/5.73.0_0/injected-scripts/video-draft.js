export const ids=["132"];export const modules={1912:function(e,i,t){t.r(i),t.d(i,{RecordingPlayer:()=>D});var r=t(52322),o=t(7184),n=t(82608),a=t(50341),s=t(77938),l=t(76524),d=t(22271),c=t(2784),u=t(49255);function h(e){return(0,r.jsx)(f,{className:e.className,children:(0,r.jsx)(m,{color:e.color??"black"})})}let f=o.Z.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 8px 12px;
`,m=o.Z.div`
  position: relative;
  margin: 0 auto;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: ${e=>u.O[e.color]};
  animation: dotFlashing 800ms infinite linear alternate;
  animation-delay: 0.4s;

  &::before,
  &::after {
    content: "";
    display: inline-block;
    position: absolute;
    top: 0;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: ${e=>u.O[e.color]};
    animation: dotFlashing 800ms infinite alternate;
  }

  &::before {
    left: -10px;
    animation-delay: 0s;
  }

  &::after {
    left: 10px;
    animation-delay: 800ms;
  }

  @keyframes dotFlashing {
    0% {
      opacity: 1;
    }
    75%,
    100% {
      opacity: 0.5;
    }
  }
`;var g=t(6663),p=t(6891),x=t(25171),v=t(70621),b=t(49710),y=t(75958),w=t(28128),j=t(20004),E=t(37079),k=t(29128),R=t(16140);let D=(0,y.Pi)(e=>{var i;let{videoDraftEvents:t,videoTrimStore:o}=e,[u,f]=(0,c.useState)(null),m=function(){let[e,i]=(0,c.useState)(null);return(0,c.useEffect)(()=>{let e=e=>{v.k.error("Detected CSP violation",{error:e}),i(e)};return document.addEventListener("securitypolicyviolation",e),()=>{document.removeEventListener("securitypolicyviolation",e)}},[]),e}(),g=(0,w.MU)(),y=(0,w.EO)(),[D,F]=function(e){let[i,t]=(0,c.useState)(null);return[i,(0,c.useCallback)(e=>{t(e)},[])]}(null),{trigger:P}=(0,w._T)(),_=(0,w.dR)(),[V,$]=(0,c.useState)(!1),A=(0,w.Pn)(),L=0===(i=e.successfulRecordingDetails).width||0===i.height?"16 / 9":`${i.width} / ${i.height}`,z=(0,j.k)(b.K8.Video);(0,c.useEffect)(()=>{if(D){let i=z();o.initializePlaybackForVideo(D,e.successfulRecordingDetails.duration,i),o.audio.setRawVideoHasAudio(_.preferences.recording.audio.on)}},[D,z,o,e.successfulRecordingDetails.duration]),(0,c.useEffect)(()=>{y.video.setVideoRef(D),v.k.debug("Writing video ref for posterImage capture",{videoEl:D}),P()},[D,y.video,P]);let I=c.useRef(!1);(0,c.useEffect)(()=>{if(I.current||!e.localBlobUrl)return;let{type:i,duration:t}=e.successfulRecordingDetails;v.k.info("video-recording-render",{type:i,duration:t}),I.current=!0},[I,e.localBlobUrl]);let O=!!e.localBlobUrl&&!u&&V&&!_.isResumedDraft();(0,p.Q)({variant:"success",interaction:"screen_recording_capture",policy:{when:"onCondition",condition:O},tags:{duration_gt_10m:e.successfulRecordingDetails.duration>n.eq("10m")}});let q=(0,s.lh)(t),J=t.filter(s.IE.video.isAnnotationEvent),K=q?.filter(e=>e.error),N=(0,s.XE)(t)??[],X=A.teamId,G=_.user?.teams.find(e=>e.id===X),H=G?.featureFlags.includes(a.J5.DisableCloudflareStream);return(0,r.jsx)(k.Z,{onSubmit:e=>(0,R.Z)({broker:g,data:e,captureType:b.K8.Video}),children:u||m?(0,r.jsxs)(c.Fragment,{children:[(0,r.jsx)(l.c,{cspViolationEvent:m??void 0,mediaError:u??void 0,verbose:!1,center:!0}),(0,r.jsx)(T,{})]}):(0,r.jsx)(c.Fragment,{children:e.localBlobUrl?(0,r.jsxs)(Z,{children:[(0,r.jsx)(S,{children:(0,r.jsx)(B,{ref:F,src:e.localBlobUrl,aspectRatio:L,onError:i=>{let t=i.currentTarget.error;t&&(f(t),v.k.error("Can't load video in the preview modal",{error:t,videoBlobUrl:e.localBlobUrl})),(0,x.Y)().finalize("screen_recording_capture","failure",{error:"video-element-error"})},onCanPlay:()=>$(!0)})}),(0,r.jsxs)(U,{children:[(0,r.jsx)(C,{children:(0,r.jsx)(d.h,{inTrimmingContext:!0,networkErrors:K,consoleErrors:N,videoAnnotationEvents:J,duration:e.successfulRecordingDetails.duration,startTimestamp:e.successfulRecordingDetails.startTimestamp})}),(0,r.jsx)(E.u,{videoTrimStore:e.videoTrimStore,showAudioButton:!1,isRewind:!1,disableTrimming:H})]})]}):(0,r.jsx)(l.d,{icon:(0,r.jsx)(h,{color:"darkGrey"}),title:"Loading preview",body:"Processing video data..."})})})}),T=()=>{let e=o.Z.div`
    position: absolute;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    text-align: center;
  `;return(0,r.jsxs)(e,{children:[(0,r.jsx)(g.x,{as:"span",weight:"bold",children:"To view the video, simply\xa0"}),(0,r.jsx)(g.x,{as:"span",weight:"bold",color:"darkLeaf",children:"create this Jam"})]})},Z=o.Z.div`
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 20px;
  justify-content: space-between;
  min-height: 0;
  min-width: 0;
  height: 100%;
`,S=o.Z.div`
  display: flex;
  flex: 1;
  justify-content: center;
  min-height: 0;
`,B=o.Z.video`
  max-width: 100%;
  max-height: 100%;
  height: auto;
  // this is super important, otherwise video will bleed out of the container
  // flex by default has min-height that is equal to the size of its content
  min-height: 0;
  aspect-ratio: ${({aspectRatio:e})=>e};
  align-self: center;
  border-radius: 12px;
  mask: linear-gradient(white, white);
`,U=o.Z.div`
  width: 100%;
`,C=o.Z.div`
  width: 100%;
  // this is necessary to align timeline events with trim controls
  padding-left: 72px;
  padding-right: 24px;
`}};
//# sourceMappingURL=video-draft.js.map