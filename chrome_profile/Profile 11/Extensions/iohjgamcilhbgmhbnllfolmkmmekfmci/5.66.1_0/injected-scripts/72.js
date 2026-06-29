export const ids=["72"];export const modules={78213:function(e,t,n){n.d(t,{h:()=>l});var r=n(52322),i=n(7184),a=n(51749),o=n(2784);let s={solid:"solid",soft:"soft",ghost:"soft",surface:"surface",outline:"outline"},l=o.forwardRef((e,t)=>{let{variant:n="solid",...i}=e;return(0,r.jsx)(d,{ref:t,variant:s[n],"data-variant":n,...i})});l.displayName="IconButton";let d=(0,i.Z)(a.h)`
  border-radius: var(--radius-3);

  // ghost variant is "soft" under the hood, we just need to override the background here
  &[data-variant="ghost"] {
    background-color: transparent;

    &:hover:not(:disabled) {
      background-color: var(--gray-a3);
    }
  }
`},75818:function(e,t,n){n.d(t,{u:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M11.9998 9v4m0 4h.01M10.6151 3.8917l-8.225 14.2066c-.4561.788-.6842 1.182-.6505 1.5054.0294.282.1772.5383.4065.7051.263.1912.7182.1912 1.6288.1912h16.4497c.9106 0 1.3658 0 1.6288-.1912a1 1 0 0 0 .4065-.7051c.0337-.3234-.1944-.7174-.6506-1.5054L13.3844 3.8917c-.4545-.7852-.6818-1.1777-.9783-1.3096a1 1 0 0 0-.8126 0c-.2966.1319-.5239.5244-.9784 1.3096",vectorEffect:"non-scaling-stroke"})})},92622:function(e,t,n){n.d(t,{J:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M20 6 9 17l-5-5",vectorEffect:"non-scaling-stroke"})})},60351:function(e,t,n){n.d(t,{b:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M3 9h13.5c2.4853 0 4.5 2.0147 4.5 4.5S18.9853 18 16.5 18H12M3 9l4-4M3 9l4 4",vectorEffect:"non-scaling-stroke"})})},32016:function(e,t,n){n.d(t,{Y:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M21 9H7.5C5.0147 9 3 11.0147 3 13.5S5.0147 18 7.5 18H12m9-9-4-4m4 4-4 4",vectorEffect:"non-scaling-stroke"})})},6891:function(e,t,n){n.d(t,{Q:()=>a});var r=n(2784),i=n(25171);function a(e){let{interaction:t,variant:n,tags:a,policy:o}=e,s="onMount"===o.when?[]:[o.condition],l=r.useRef(!1);r.useEffect(()=>{!l.current&&("onCondition"!==o.when||o.condition)&&(l.current=!0,"failure"===n?(0,i.Y)().finalize(t,"failure",{error:e.error,tags:a}):(0,i.Y)().finalize(t,n,{tags:a}))},s)}},76502:function(e,t,n){n.d(t,{Z:()=>np});var r=n(52322),i=n(7184),a=n(82608),o=n(6648),s=n(63403),l=n(25171),d=n(70621),c=n(75958),u=n(2784),p=n(28316),g=n(28128),m=n(20322);let x={gracePeriodMs:2e3};var h=n(71509),f=n(80075);async function b(e,t,n){t.setTeamId(n),t.setIsLoading(!0);let r=await e.send({eventName:"GetFolders",data:{teamId:n},dest:{component:s.wA.Main,location:void 0}}).finally(()=>t.setIsLoading(!1));return r&&t.replaceFolders(r.map(e=>({id:e.id,name:e.name,teamId:e.teamId,lastChangedAt:new Date(e.lastChangedAt),quantity:e.quantity}))),t.availableFolders}function v(e,t,n){try{e()}catch(e){d.k.error(`error on ${t}`,{error:(0,h.LT)(e),...n})}}let w=(e,t=a.eq("10s"))=>new Promise((n,r)=>{if(!e.availableIntegrationsLoading){n();return}let i=setTimeout(()=>{a(),r(Error(`Timeout waiting for integrations to load after ${t}ms`))},t),a=(0,f.U5)(()=>e.availableIntegrationsLoading,e=>{e||(clearTimeout(i),a(),n())})});async function y(e,t,n){if(!t?.integrationName)return;await w(e);let r=e.getIntegration(t.integrationName,n);r&&(e.setSelectedIntegration(n,r),t.displayFieldsFilters&&Object.entries(t.displayFieldsFilters).forEach(([n,r])=>{n===t.integrationName&&e.setDisplayFieldsFilters(n,r)}),await e.fetchDisplayFieldsForSelectedIntegration(),Object.entries(t.fieldValues).forEach(([t,n])=>{e.displayFields.get(t)&&e.setFieldValue(t,n)}))}async function C(e,t,n,r){r&&((await b(e,t,n)).find(e=>e.id===r)?t.selectFolderById(r):d.k.warn("cannot resume selected folder, no avialable folder with id",{folderId:r}))}let S=()=>{let e=(0,g.Pn)(),t=(0,u.useCallback)(async()=>{e.syncSelectedTeamIntegrationDown(),await e.clearSelectedIntegrationContext(),e.syncContextDown()},[e]),n=(0,u.useCallback)(()=>{e.syncContextUp()},[e]);return(0,u.useEffect)(()=>{(async()=>{await e.syncedDataStore.fetchSyncedTeamIntegrationData(),t()})()},[e.syncedDataStore,t]),n};var j=n(33735);let k=()=>{let{teamFeatureUsage:e}=(0,g.dR)(),t=(0,g.$7)().selectedTeamId,n=e.get(t,j.AN.TeamJamQuotaLimit),r=!!(n&&n.limit>-1&&n.remaining<=5),i=!!(n&&n.limit>-1&&n.current>=n.limit);return{teamId:t,jamQuotaUsage:n,shouldShowWarning:r,hasReachedLimit:i}};var I=n(76062),$=n(88767);async function A(e){let t=await new Promise((t,n)=>{let r=new FileReader;r.readAsDataURL(e),r.addEventListener("load",()=>{r.result&&t(r.result.toString())}),r.addEventListener("error",e=>{n(e)})});return{id:$.Z(),source:t,type:e.type,name:e.name,size:e.size}}var N=n(25016),T=n(27300),R=n(78213),z=n(87722),M=n(30199);let L=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M20 7v-.2c0-1.6802 0-2.5202-.327-3.162a3 3 0 0 0-1.311-1.311C17.7202 2 16.8802 2 15.2 2H8.8c-1.6802 0-2.5202 0-3.162.327a3 3 0 0 0-1.311 1.311C4 4.2798 4 5.1198 4 6.8v10.4c0 1.6802 0 2.5202.327 3.162a3 3 0 0 0 1.311 1.311C6.2798 22 7.1198 22 8.8 22h3.7m5.5-4v-5.5c0-.8284.6716-1.5 1.5-1.5s1.5.6716 1.5 1.5V18c0 1.6569-1.3431 3-3 3s-3-1.3431-3-3v-4",vectorEffect:"non-scaling-stroke"})});var P=n(99692);function Z(e){let{attachments:t,onRemove:n,downloadable:i,optimizeImageUrl:a}=e;return 0===t.length?null:(0,r.jsx)(N.k,{gap:"2",p:"2",children:t.map(e=>{let t=e.name.slice(e.name.lastIndexOf(".")+1),o=e.type.startsWith("image/"),s=a?a(e.src,{width:168}):e.src,l=o?(0,r.jsx)(E,{children:(0,r.jsx)("img",{src:s,alt:e.name})}):(0,r.jsxs)(F,{direction:"column",align:"center",justify:"center",pt:"1",children:[(0,r.jsx)(L,{}),(0,r.jsx)(M.x,{as:"span",variant:"label-xs",children:"."+t})]});return(0,r.jsxs)(D,{children:[(0,r.jsx)(T.u,{sideOffset:10,content:e.name,children:i?(0,r.jsx)(O,{target:"_blank",href:e.src,download:e.name,children:l}):l}),n&&(0,r.jsx)(U,{size:"1",color:"gray",variant:"solid",onClick:()=>n(e.id),children:(0,r.jsx)(P.A,{size:12})})]},e.id)})})}let D=(0,i.Z)(N.k)`
  position: relative;
`,O=i.Z.a`
  cursor: pointer;
  text-decoration: none;
  color: inherit;
`,E=(0,i.Z)(N.k)`
  border-radius: var(--radius-3);
  box-shadow: var(--shadow-3);
  overflow: hidden;

  img {
    width: 56px;
    height: 56px;
    object-fit: cover;
  }
`,F=(0,i.Z)(N.k)`
  width: 56px;
  height: 56px;
  border-radius: var(--radius-3);
  background: var(--gray-a3);
  color: var(--gray-11);
`,U=(0,i.Z)(R.h)`
  position: absolute;
  top: -6px;
  right: -6px;
  background: var(--gray-12);
  box-shadow: 0 0 0 2px var(--color-background);
  border-radius: var(--radius-5);
  width: 16px;
  height: 16px;
  transform: rotate(0);
  transition: transform 300ms;

  &:hover,
  &:focus {
    background: var(--red-11);
    transform: rotate(90deg) scale(1.2);
    box-shadow: 0 0 0 2px var(--red-a5);
    outline: none;
    outline-offset: 0;
  }
`;var W=n(62563),B=n(2350);let G="file-drop-over";function J(e){let t=e.dataTransfer;return!!t&&(t.files.length>0||Array.from(t.types).includes("Files"))}var H=n(1389),_=n(70822),V=n(34220);let Y=W.hj.create({name:"titlePlaceholder",addOptions:()=>({forceFocusDelay:null}),onCreate({editor:e}){e.commands.focus(q(e));let{forceFocusDelay:t}=this.options;null!==t&&setTimeout(()=>{e.isDestroyed||e.commands.focus(q(e))},t)},addProseMirrorPlugins:()=>[new B.Sy({key:new B.H$("sendToAppPlaceholder"),props:{decorations(e){let{doc:t}=e,n=[],r=!1,i=!1;return t.forEach((e,t,n)=>{0===n&&"heading"===e.type.name&&(r=!0),n>0&&e.childCount>0&&(i=!0)}),t.forEach((e,t,a)=>{var o,s,l;if(e.childCount>0)return;let d=(o=e,s=a,l={hasHeading:r,hasBodyContent:i},0===s&&"heading"===o.type.name?"Title":"paragraph"!==o.type.name||l.hasBodyContent?null:1!==s&&(0!==s||l.hasHeading)?null:"Write a description or @ to mention");d&&n.push(_.p.node(t,t+e.nodeSize,{class:"is-empty","data-placeholder":d}))}),_.EH.create(t,n)}}})]});function q(e){return"disabled"!==(0,V.yt)(e)?"start":e.getText().trim().length>0?"end":"start"}var K=n(47209),Q=n(25755);let X=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M17.5 5.2558V16.5c0 3.0376-2.4624 5.5-5.5 5.5s-5.5-2.4624-5.5-5.5V5.6667C6.5 3.6417 8.1416 2 10.1667 2c2.025 0 3.6666 1.6416 3.6666 3.6667v10.779c0 1.0126-.8208 1.8334-1.8333 1.8334s-1.8333-.8208-1.8333-1.8334V6.6512",vectorEffect:"non-scaling-stroke"})});var ee=n(20305),et=n(50194),en=n(7656);let er=(0,en.T)({BR000:"0px",BR050:"2px",BR075:"4px",BR100:"8px",BR200:"10px",BR210:"12px",BR300:"16px",BR400:"20px",BR600:"40px",BR900:"70px",BRROUND:"99999px",BROVAL:"50%"});var ei=n(49255),ea=n(32748),eo=n(32760),es=n(76556),el=n(6663);let ed=(0,c.Pi)(function(e){let{onUpgrade:t,isDismissable:n,feature:i}=e,[a,o]=u.useState(!1);return a||!e.shouldShow()?null:(0,r.jsxs)(ec,{children:[(0,r.jsx)(ep,{size:"bodyMedium",color:"black",weight:"medium",children:e.text()}),(0,r.jsx)(eu,{onClick:()=>t(i),size:"small",variant:"solid",appearance:"light",textType:"body",rounded:!1,children:"Upgrade"}),n()?(0,r.jsx)(eg,{role:"button",tabIndex:0,onClick:()=>o(!0),children:(0,r.jsx)(P.A,{size:12,style:{color:ei.O.charcoalGrey}})}):null]})}),ec=i.Z.div`
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${eo.W.SP150};
  background-color: #E1F6FD;
  border-radius: ${er.BR200};
  width: 100%;
`,eu=(0,i.Z)(es.z)`
  margin-left: auto;
  font-weight: ${ea.v.medium};
`,ep=(0,i.Z)(el.x)`
  padding: 0px ${eo.W.SP200};
`,eg=i.Z.div`
  position: absolute;
  right: -10px;
  top: -10px;
  border-radius: 100%;
  background-color: ${ei.O.nearWhite};
  border: 1px solid #6666;
  padding: 2px;
  display: flex;
  box-shadow: lch(0 0 0 / 0.022) 0px 6px 18px, lch(0 0 0 / 0.044) 0px 3px 9px, lch(0 0 0 / 0.044) 0px 1px 1px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;

  &:hover {
    svg {
      color: ${ei.O.black};
    }
  }
`,em=e=>e.numDemoUsesRemaining??e.store.numDemoUsesRemaining(e.feature),ex=(0,c.Pi)(function(e){let[t,n]=u.useState(!1);if(t||e.store?.hasAccess(e.feature,e.teamId??"any"))return null;let i=em(e),a=j.ZY[e.feature];return(0,r.jsxs)(eh,{children:[(0,r.jsx)(eb,{size:"bodyMedium",color:"black",weight:"medium",children:e.text(i,a)}),(0,r.jsx)(ef,{onClick:()=>e.onUpgrade(e.feature),size:"small",variant:"solid",appearance:"light",textType:"body",rounded:!1,children:"Upgrade"}),e.dismissable&&0===i?(0,r.jsx)(ev,{role:"button",tabIndex:0,onClick:()=>n(!0),children:(0,r.jsx)(P.A,{size:16})}):null]})}),eh=i.Z.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${eo.W.SP150};
  background-color: #f2ecfe;
  border-radius: ${er.BR200};
  width: 100%;
`,ef=(0,i.Z)(es.z)`
  margin-left: auto;
  font-weight: ${ea.v.medium};
`,eb=(0,i.Z)(el.x)`
  padding: 0px ${eo.W.SP200};
`,ev=i.Z.div`
  padding: 0px ${eo.W.SP200};
  cursor: pointer;
`;var ew=n(61525),ey=n(72321),eC=n(884);function eS(e,t,n){ey._z.info("Redirecting to upgrade flow",{teamId:e,feature:t});let r=new URL("s/upgrade",eC.v.DASH_URL);r.search=new URLSearchParams({[I.t1.CAMPAIGN]:t,...n}).toString(),window.open(r.toString(),"_blank")}var ej=n(49710),ek=n(84869),eI=n.n(ek);function e$(e){if(!e)return"Unknown User";let t=e.firstName?.trim(),n=e.lastName?.trim();if(t&&n)return`${t} ${n}`;if(t)return t;if(n)return n;let r=e.name?.trim();if(r)return r;let i=e.email?.trim();if(i){let e=i.split("@")[0];if(e)return e}return"Unknown User"}var eA=n(79976),eN=n(42494);let eT=new B.H$("jamMentionSuggestion"),eR=(0,i.Z)(eA.q)`
  padding: calc(var(--space-1) / 2);
`,ez=(0,i.Z)(M.x)`
  line-height: 20px;
  height: 20px;
`;var eM=n(75514);function eL(e){if(null==e)return 0;let t=new Date(e).getTime();return Number.isFinite(t)?t:0}let eP=(0,en.T)({SHADOW1:"0px 8px 8px -4px rgba(64, 1, 17, 0.02), 0px 4px 4px -2px rgba(64, 1, 17, 0.02), 0px 2px 2px -1px rgba(42, 51, 69, 0.01), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.01), 0px 0.5px 0.5px -0.25px rgba(42, 51, 69, 0.01), 0px 0px 0px 1px rgba(64, 1, 17, 0.01)",SHADOW2:"0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(64, 1, 17, 0.0156863), 0px 4px 4px -2px rgba(42, 51, 69, 0.0156863), 0px 2px 2px -1px rgba(42, 51, 69, 0.0156863), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.0156863), 0px 0px 0px 1px rgba(64, 1, 17, 0.0156863)",SHADOW3:"0px 24px 24px -12px rgba(64, 1, 17, 0.0470588), 0px 12px 12px -6px rgba(64, 1, 17, 0.0235294), 0px 6px 6px -3px rgba(42, 51, 69, 0.0235294), 0px 3px 3px -1.5px rgba(42, 51, 69, 0.0235294), 0px 1.5px 1.5px -0.75px rgba(42, 51, 69, 0.0235294), 0px 0px 0px 1px rgba(64, 1, 17, 0.0235294)",SHADOW4:"0px 32px 32px -16px rgba(64, 1, 17, 0.0627451), 0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(42, 51, 69, 0.0313726), 0px 4px 4px -2px rgba(42, 51, 69, 0.0313726), 0px 2px 2px -1px rgba(42, 51, 69, 0.0313726), 0px 0px 0px 1px rgba(64, 1, 17, 0.0313726)",SHADOW5:"0px 24px 24px -12px rgba(64, 1, 17, 0.0627451), 0px 12px 12px -6px rgba(64, 1, 17, 0.0313726), 0px 6px 6px -3px rgba(42, 51, 70, 0.0313726), 0px 3px 3px -1.5px rgba(42, 51, 70, 0.0313726), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.0313726), 0px 0px 0px 1px rgba(64, 1, 17, 0.0313726)",SHADOW6:"0px 32px 32px -16px rgba(64, 1, 17, 0.0627451), 0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(42, 51, 69, 0.0313726), 0px 4px 4px -2px rgba(42, 51, 69, 0.0313726), 0px 2px 2px -1px rgba(42, 51, 69, 0.0313726), 0px 0px 0px 1px rgba(64, 1, 17, 0.0313726)",SHADOW7:"0px 24px 24px -12px rgba(64, 1, 17, 0.0470588), 0px 12px 12px -6px rgba(64, 1, 17, 0.0235294), 0px 6px 6px -3px rgba(42, 51, 69, 0.0235294), 0px 3px 3px -1.5px rgba(42, 51, 69, 0.0235294), 0px 1.5px 1.5px -0.75px rgba(42, 51, 69, 0.0235294), 0px 0px 0px 1px rgba(64, 1, 17, 0.0235294)",SHADOW8:"0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(64, 1, 17, 0.0156863), 0px 4px 4px -2px rgba(42, 51, 69, 0.0156863), 0px 2px 2px -1px rgba(42, 51, 69, 0.0156863), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.0156863), 0px 0px 0px 1px rgba(64, 1, 17, 0.0156863)",SHADOW9:"0px 8px 8px -4px rgba(64, 1, 17, 0.02), 0px 4px 4px -2px rgba(64, 1, 17, 0.02), 0px 2px 2px -1px rgba(42, 51, 69, 0.01), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.01), 0px 0.5px 0.5px -0.25px rgba(42, 51, 69, 0.01), 0px 0px 0px 1px rgba(64, 1, 17, 0.01)"}),eZ=i.Z.div`
  align-self: stretch;
  display: flex;
  align-items: center;
  margin-bottom: ${eo.W.SP600};
`,eD=i.Z.button`
  display: flex;
  height: 40px;
  justify-content: center;
  align-items: center;
  gap: ${eo.W.SP200};
  padding: ${eo.W.SP200} ${eo.W.SP300};
  border-radius: ${er.BR100};
  background: ${ei.O.white};
  box-shadow: ${eP.SHADOW2}, 0px 0px 0px 1px rgba(0, 0, 0, 0.03);
`,eO=function(e){let{closeJam:t,resumedDraft:n}=e;return(0,r.jsx)(eZ,{children:(0,r.jsxs)(eD,{onClick:function(e){e.stopPropagation(),t()},children:[(0,r.jsx)(P.A,{color:ei.O.charcoalGrey,size:16}),n&&(0,r.jsx)(M.x,{variant:"label-s",color:"primary",children:"Save for later"})]})})};function eE(e){return(0,r.jsxs)(eF,{className:e.className,children:[(0,r.jsx)(eU,{color:e.color}),(0,r.jsx)(eU,{color:e.color}),(0,r.jsx)(eU,{color:e.color})]})}let eF=i.Z.div`
  display: flex;
  align-items: center;
`,eU=i.Z.span`
  display: inline-block;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  margin-right: 2px;
  background: ${e=>ei.O[e.color]};
  animation: wave 1s ease-in-out infinite;
  animation-delay: 0.5s;

  &:nth-child(2) {
    animation-delay: -0.6s;
  }

  &:nth-child(3) {
    animation-delay: -0.7s;
  }

  @keyframes wave {
    0%,
    60%,
    100% {
      transform: initial;
      opacity: initial;
    }

    30% {
      transform: translateY(-2px);
      opacity: 0.3;
    }
  }
`;var eW=n(17029);let eB=()=>(0,r.jsxs)(eG,{type:"button",children:[(0,r.jsx)(eH,{children:"Accept"})," ",(0,r.jsx)(eJ,{children:"Tab"})]}),eG=i.Z.button`
  display: flex;
  height: 32px;
  align-items: center;
  font-size: 14px;
  background: white;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.25);
  border-radius: 9px;
  color: rgba(0, 0, 0, 1);
  gap: 8px;
  margin-top: 8px;
  padding: 0 12px;
  padding-right: 8px;

  &:hover {
    cursor: pointer;
    box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.4);
  }
`,eJ=i.Z.kbd`
  display: flex;
  height: 16px;
  line-height: 16px;
  background: rgba(0, 0, 0, 0.04);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  font-size: 11px;
  padding: 0 4px;
`,eH=i.Z.span`
  line-height: 32px;
  font-size: 14px;
`,e_=V.Vb.configure({renderAcceptButton:function(e){let t=document.createElement("div");return t.className="ghost-text-accept",t.addEventListener("mousedown",t=>{t.preventDefault(),e()}),(0,eW.createRoot)(t).render(u.createElement(eB)),t},renderSpinner:function(){let e=document.createElement("div");return e.className="ghost-text-loader",(0,eW.createRoot)(e).render(u.createElement(eE,{color:"darkGrape"})),e}});var eV=n(94338);let eY=({highContrast:e=!0,...t})=>(0,r.jsx)(eV.r,{highContrast:e,...t});function eq(e){return(0,r.jsxs)(N.k,{align:"center",gap:"2",mx:"1",children:[(0,r.jsx)(M.x,{variant:"label-s",children:"AI"}),(0,r.jsx)(T.u,{content:e.lockedReason,hidden:!e.locked,children:(0,r.jsx)(eY,{size:"1",checked:e.enabled,disabled:e.locked,onCheckedChange:e.onChange})})]})}var eK=n(37105);let eQ=(0,i.Z)(eK.ck)`
  /* Default state styling */
  &.rt-DropdownMenuItem {
    font-weight: var(--font-weight-medium);
  }

  /* Unified hover state - works for any color, defaults to gray */
  &.rt-DropdownMenuItem:hover {
    ${e=>`background-color: var(--${e.color||"gray"}-a3);`}
  }
`,eX=(0,i.Z)(eK.fF)`
  /* SubTrigger font-weight override */
  &.rt-DropdownMenuSubTrigger {
    font-weight: var(--font-weight-medium);
  }

  /* Unified hover state - works for any color, defaults to gray */
  &.rt-DropdownMenuSubTrigger:hover {
    ${e=>`background-color: var(--${e.color||"gray"}-a3);`}
  }
`,e0=(0,i.Z)(eK.tu)`
  /* SubContent items font-weight override */
  .rt-DropdownMenuItem {
    font-weight: var(--font-weight-medium);
  }
`,e1=u.forwardRef((e,t)=>{let{color:n="gray",...i}=e;return(0,r.jsx)(eK.VY,{ref:t,variant:"soft",color:n,...i})});e1.displayName="DropdownMenuContent";let e2={Root:eK.fC,Trigger:eK.xz,Content:e1,Item:eQ,Separator:eK.Z0,Label:eK.__,Sub:eK.Tr,SubTrigger:eX,SubContent:e0,RadioGroup:eK.Ee,RadioItem:eK.Rk},e5=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"m13 7-1.1155-2.231c-.3211-.6422-.4816-.9633-.7211-1.1978a2 2 0 0 0-.7473-.4619C10.0992 3 9.7402 3 9.0223 3H5.2c-1.1201 0-1.6802 0-2.108.218a2 2 0 0 0-.874.874C2 4.5198 2 5.08 2 6.2V7m0 0h15.2c1.6802 0 2.5202 0 3.162.327a3 3 0 0 1 1.311 1.311C22 9.2798 22 10.1198 22 11.8v4.4c0 1.6802 0 2.5202-.327 3.162a3 3 0 0 1-1.311 1.311C19.7202 21 18.8802 21 17.2 21H6.8c-1.6802 0-2.5202 0-3.162-.327a3 3 0 0 1-1.311-1.311C2 18.7202 2 17.8802 2 16.2z",vectorEffect:"non-scaling-stroke"})}),e6=(0,c.Pi)(e=>{let{foldersStore:t}=e,n=t.availableFolders,i=t.selectedFolder;return 0===n.length?null:(0,r.jsxs)(e2.Root,{children:[(0,r.jsx)(T.u,{content:"Select folder",children:(0,r.jsx)(e2.Trigger,{children:i?(0,r.jsxs)(e3,{size:"1",variant:"ghost",color:"gray",children:[(0,r.jsx)(N.k,{flexShrink:"0",children:(0,r.jsx)(e5,{size:16})}),(0,r.jsx)(M.x,{truncate:!0,variant:"label-s",children:i.name})]}):(0,r.jsx)(R.h,{size:"1",variant:"ghost",color:"gray",children:(0,r.jsx)(e5,{size:16})})})}),(0,r.jsxs)(e2.Content,{children:[(0,r.jsx)(e2.Item,{onSelect:()=>t.selectFolderById(),children:"No folder"}),n.map(e=>(0,r.jsx)(e2.Item,{onSelect:()=>t.selectFolderById(e.id),children:(0,r.jsxs)(N.k,{gap:"2",align:"center",children:[(0,r.jsx)(e5,{}),(0,r.jsx)(M.x,{children:e.name})]})},e.id))]})]})});e6.displayName="DraftFolderSelect";let e3=(0,i.Z)(z.z)`
  display: flex;
  flex: 0 1 auto;
  min-width: 0;
  white-space: nowrap;
  text-overflow: ellipsis;
`;var e4=n(72986),e7=n(3311);let e9=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M9 17H7c-2.7614 0-5-2.2386-5-5s2.2386-5 5-5h2m6 10h2c2.7614 0 5-2.2386 5-5s-2.2386-5-5-5h-2m-8 5h10",vectorEffect:"non-scaling-stroke"})});var e8=n(22970),te=n(28165);let tt=i.Z.div`
  ${function(e){return(0,te.iv)`
    padding: ${e.padding};
    margin: ${e.margin};
    background: ${ei.O[e.background]};
    border-radius: ${e.borderRadius};
    border: ${e.borderColor?`1px solid ${ei.O[e.borderColor]}`:"none"};
  `}}
`;function tn(e,t){if(t)return Array.isArray(t)?t.map(t=>e[t]).join(" "):e[t]}function tr(e){let{align:t,alignSelf:n,justify:i,direction:a,gap:o,wrap:s,grow:l,shrink:d,basis:c,dir:u,inline:p,width:g,...m}=e,x={align:t,justify:i,direction:u??a,alignSelf:n,gap:o&&eo.W[o],wrap:s,grow:l,shrink:d,basis:c,inline:p,width:g,className:e.className??void 0};return(0,r.jsx)(ti,{...x,...m,children:e.children})}let ti=(0,i.Z)(function(e){let t={padding:tn(eo.W,e.padding),margin:tn(eo.W,e.margin),background:e.background??"transparent",borderRadius:tn(er,e.borderRadius),borderColor:e.borderColor};return(0,r.jsx)(tt,{...t,className:e.className,children:e.children})})`
  display: ${e=>e.inline?"inline-flex":"flex"};
  ${function(e){return(0,te.iv)`
    align-items: ${e.align};
    align-self: ${e.alignSelf??"initial"};
    justify-content: ${e.justify};
    flex-direction: ${e.direction};
    flex-grow: ${e.grow??"initial"};
    flex-shrink: ${e.shrink??"initial"};
    flex-basis: ${e.basis??"initial"};
    gap: ${e.gap};
    flex-wrap: ${e.wrap??"initial"};
    width: ${e.width??"auto"};
  `}}
`;function ta(e){let{fillStroke:t="#2A3632",...n}=e;return(0,r.jsxs)(to,{...n,viewBox:"0 0 18 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,r.jsx)("path",{d:"M11.609 15.4909C11.018 15.25 10.4089 15 8.99986 15C7.59077 15 6.97713 15.25 6.39077 15.4909C6.22259 15.5591 6.04986 15.6273 5.86349 15.6909C5.38168 16.2682 5.15895 17.0636 5.27258 17.8364C5.33622 18.2773 5.72258 18.6091 6.17258 18.6091C6.21804 18.6091 6.26349 18.6045 6.31349 18.6C6.77258 18.5318 7.12258 18.3636 7.38622 18.1818C7.57713 18.6318 7.94077 19.1364 8.64531 19.4409C8.75895 19.4909 8.87713 19.5136 9.0044 19.5136C9.13168 19.5136 9.24986 19.4909 9.36349 19.4409C10.068 19.1409 10.4317 18.6318 10.6226 18.1818C10.8862 18.3636 11.2362 18.5273 11.6953 18.6C11.7408 18.6091 11.7862 18.6091 11.8362 18.6091C12.2862 18.6091 12.6726 18.2773 12.7362 17.8364C12.8453 17.0636 12.6271 16.2682 12.1453 15.6909C11.9499 15.6273 11.7817 15.5591 11.609 15.4909Z",fill:"#73E5BF"}),(0,r.jsx)("path",{d:"M13.5454 15.9091C12.6409 15.9091 12.1182 15.6954 11.6091 15.4909C11.0182 15.25 10.4091 15 8.99998 15C7.59089 15 6.97725 15.25 6.39089 15.4909C5.88634 15.6954 5.36361 15.9091 4.45452 15.9091C3.4227 15.9091 2.62725 15.6363 2.08634 15.0954C1.54543 14.5545 1.27271 13.7591 1.27271 12.7273C1.27271 10.0409 2.14543 6.97726 3.60907 4.54089C5.16816 1.94544 7.1318 0.454529 8.99998 0.454529C10.8682 0.454529 12.8318 1.94544 14.3909 4.54089C15.8545 6.9818 16.7273 10.0409 16.7273 12.7273C16.7273 13.7591 16.4545 14.5545 15.9136 15.0954C15.3727 15.6363 14.5772 15.9091 13.5454 15.9091Z",fill:"#FF4070"}),(0,r.jsx)("path",{d:"M6.95452 9.09089C6.72725 9.09089 6.27271 9.09089 6.27271 10.2273C6.27271 11.3636 6.72725 11.3636 6.95452 11.3636C7.1818 11.3636 7.63634 11.3636 7.63634 10.2273C7.63634 9.09089 7.1818 9.09089 6.95452 9.09089Z",fill:t}),(0,r.jsx)("path",{d:"M11.0454 9.09089C10.8182 9.09089 10.3636 9.09089 10.3636 10.2273C10.3636 11.3636 10.8182 11.3636 11.0454 11.3636C11.2727 11.3636 11.7273 11.3636 11.7273 10.2273C11.7273 9.09089 11.2727 9.09089 11.0454 9.09089Z",fill:t}),(0,r.jsx)("path",{d:"M8.99998 5.45453C8.77271 5.45453 8.31816 5.45453 8.31816 6.59089C8.31816 7.72726 8.77271 7.72726 8.99998 7.72726C9.22725 7.72726 9.6818 7.72726 9.6818 6.59089C9.6818 5.45453 9.22725 5.45453 8.99998 5.45453Z",fill:t}),(0,r.jsx)("path",{d:"M16.5228 8.32273C16.1091 6.9 15.5046 5.50909 14.7819 4.30455C14.0319 3.05455 13.1546 2.00909 12.241 1.27727C11.1773 0.431818 10.0864 0 9.00006 0C7.91369 0 6.82278 0.431818 5.76369 1.27727C4.85005 2.00909 3.97278 3.05455 3.22278 4.30455C2.50006 5.50909 1.89551 6.9 1.48187 8.32273C1.04551 9.80909 0.818237 11.3318 0.818237 12.7273C0.818237 13.8818 1.13642 14.7864 1.76824 15.4136C2.39551 16.0455 3.30006 16.3636 4.4546 16.3636C4.64551 16.3636 4.81824 16.3545 4.98187 16.3409C4.8046 16.8318 4.74551 17.3727 4.82278 17.9C4.91824 18.5636 5.50005 19.0636 6.17278 19.0636C6.24096 19.0636 6.31369 19.0591 6.38187 19.0455C6.69551 18.9955 6.97278 18.9091 7.2046 18.8045C7.5046 19.2682 7.93187 19.6273 8.46369 19.8545C8.63642 19.9273 8.81369 19.9636 9.00006 19.9636C9.18642 19.9636 9.36824 19.9273 9.53642 19.8545C10.0682 19.6273 10.4955 19.2682 10.7955 18.8045C11.0319 18.9091 11.3046 18.9955 11.6182 19.0455C11.6864 19.0545 11.7591 19.0591 11.8273 19.0591C12.5001 19.0591 13.0819 18.5591 13.1773 17.8955C13.2546 17.3682 13.1955 16.8273 13.0182 16.3364C13.1819 16.35 13.3546 16.3591 13.5455 16.3591C14.7001 16.3591 15.6046 16.0409 16.2319 15.4091C16.8637 14.7864 17.1819 13.8818 17.1819 12.7273C17.1819 11.3318 16.9546 9.80909 16.5228 8.32273ZM12.2773 17.7682C12.2455 17.9955 12.0501 18.1545 11.8273 18.1545C11.8046 18.1545 11.7819 18.1545 11.7591 18.15C10.7228 17.9909 10.3637 17.2727 10.3637 17.2727C10.3637 17.2727 10.3637 18.5136 9.17733 19.0227C9.11824 19.0455 9.05915 19.0591 9.00006 19.0591C8.94096 19.0591 8.87733 19.0455 8.82278 19.0227C7.63642 18.5136 7.63642 17.2727 7.63642 17.2727C7.63642 17.2727 7.27733 17.9909 6.24096 18.15C6.21824 18.1545 6.19551 18.1545 6.17278 18.1545C5.95005 18.1545 5.7546 17.9955 5.72278 17.7682C5.63187 17.1227 5.81824 16.5091 6.13642 16.0727C6.28642 16.0182 6.42733 15.9636 6.55915 15.9091C7.13187 15.6727 7.67733 15.4545 9.00006 15.4545C10.3228 15.4545 10.8637 15.6773 11.441 15.9091C11.5773 15.9636 11.7137 16.0227 11.8637 16.0727C12.1819 16.5091 12.3728 17.1227 12.2773 17.7682ZM13.5455 15.4545C11.7273 15.4545 11.7273 14.5455 9.00006 14.5455C6.27278 14.5455 6.27278 15.4545 4.4546 15.4545C2.63642 15.4545 1.72733 14.5455 1.72733 12.7273C1.72733 7.27273 5.36369 0.909091 9.00006 0.909091C12.6364 0.909091 16.2728 7.27273 16.2728 12.7273C16.2728 14.5455 15.3637 15.4545 13.5455 15.4545Z",fill:t})]})}let to=i.Z.svg`
  vertical-align: middle;
`;function ts(e){return(0,r.jsx)(tl,{autoMargin:e.autoMargin??!0,className:e.className,children:(0,r.jsx)(ta,{height:24,width:24})})}let tl=i.Z.div`
  padding: initial;
  ${e=>e.autoMargin&&"margin: 0 auto;"}
  text-align: center;
  width: 24px;
  animation: spin 700ms ease-in-out infinite;

  @keyframes spin {
    0% {
      transform: rotateZ(0deg);
    }
    100% {
      transform: rotateZ(360deg);
    }
  }
`;var td=n(6757);let tc=i.Z.button`
  display: grid;
  align-items: center;
  grid-template-columns: 24px 20px;
  border-radius: ${eo.W.SP200};
  padding: ${eo.W.SP200} ${eo.W.SP250};
  gap: ${eo.W.SP200};
  background: ${ei.O.white};
  border: 1px solid ${ei.O.mediumGrey};
  box-shadow: ${eP.SHADOW1};
`,tu=i.Z.div`
  background: ${ei.O.black};
  display: flex;
  flex-direction: column;
  max-width: 260px;
  width: 100%;
  overflow: hidden;
  padding: ${eo.W.SP100};
`,tp=i.Z.button`
  width: 100%;
  background: transparent;
  padding: ${eo.W.SP100} ${eo.W.SP400};
  display: grid;
  align-items: center;
  border-radius: 8px;
  flex: none;
  min-height: 40px;
  height: 40px;
  grid-template-columns: 24px minmax(0, 1fr) 20px;
  gap: 12px;
  text-align: left;
  transition: none;

  &:hover {
    background: ${ei.O.nearBlack};
  }
`,tg=i.Z.div`
  height: 1px;
  background: ${ei.O.nearBlack};
  margin: ${eo.W.SP200} ${eo.W.SP400};
`;var tm=n(40807),tx=n(59802),th=n(17620),tf=n.n(th),tb=n(75818),tv=n(92622),tw=n(89825);let ty=(0,c.Pi)(function(e){let{integration:t,unlocked:n=!0}=e,i=t.userConfigured&&t.teamConfigured,a=!i&&!t.allowConnecting,o=(0,r.jsxs)(tj,{disabled:!n||!t.allowConnecting&&!i,onClick:e.onClick,children:[e.icon??null,(0,r.jsx)(tC,{unlocked:n,integration:t,isConfigured:i}),e.active&&(0,r.jsx)(tv.J,{color:n?ei.O.white:ei.O.darkGrey}),a&&(0,r.jsx)(tb.u,{color:ei.O.mango})]},t.integrationName);return a?(0,r.jsx)(tw.u,{title:(0,e4.w5)(t.displayName),children:o}):o});function tC(e){let t=e.integration.integrationName,n=(0,e4._g)(t),i=e.integration.displayName,a="darkGrey";return(e.isConfigured&&(a=e.unlocked?"white":"darkGrey"),e.isConfigured)?(0,r.jsx)(tS,{color:a,children:i+" "+n}):(0,r.jsxs)(tr,{gap:"SP100",children:[(0,r.jsx)(el.x,{as:"span",color:a,weight:"regular",size:"bodyMedium",children:"Connect"}),(0,r.jsx)(tS,{color:a,children:i})]})}let tS=(0,i.Z)(e=>(0,r.jsx)(el.x,{as:"span",weight:"regular",size:"bodyMedium",...tf()(e,"unlocked")}))``,tj=(0,i.Z)(e=>(0,r.jsx)(tp,{...tf()(e,"$isConfigured")}))`
  grid-template-columns: 20px minmax(0, 1fr) 20px;

  svg:first-of-type {
    display: block;
    width: 20px;
  }

  &:disabled svg:first-of-type {
    filter: grayscale(1) sepia(0.8) saturate(0) brightness(0.7);
  }
`,tk={userConfigured:!0,teamConfigured:!0,allowConnecting:!0,integrationName:"link",displayName:"Link to share"},tI=(0,c.Pi)(e=>{let{excludeInternalIntegrations:t,teamEntitlements:n,integrations:i,onSelectIntegration:a,onClearSelectedIntegration:o,onConnectMoreApps:s,excludeEmailIntegration:l,excludeLinkOption:d}=e,c={teamId:e.teamId,integrations:i,onSelectIntegration:a,onClearSelectedIntegration:o,onConnectMoreApps:s,excludeInternalIntegrations:t,excludeEmailIntegration:l,excludeLinkOption:d,hasEntitlement:n.has};return(0,r.jsx)(t$,{...c})}),t$=(0,c.Pi)(e=>{let t=e.integrations.userConfiguredIntegrationsExcludingEmail(e.teamId)>=2,n=e.integrations.selectedIntegrationPerTeam.get(e.teamId);return(0,r.jsxs)(u.Fragment,{children:[e.excludeLinkOption?null:(0,r.jsx)(ty,{active:!n,unlocked:!0,integration:tk,icon:(0,r.jsx)(e9,{color:"white",size:20}),onClick:e.onClearSelectedIntegration}),(0,r.jsx)(()=>{let i=e.integrations.getBy(e.teamId,{filterBy:"dataPushNotIssueTracker",sortBy:"standard"}).filter(t=>!e.excludeInternalIntegrations||!t.internal).filter(t=>!e.excludeEmailIntegration||"email"!==t.integrationName).filter(e=>"intercom"!==e.integrationName).filter(e=>!t||e.userConfigured);return(0,r.jsx)(r.Fragment,{children:i.map(t=>(0,r.jsx)(ty,{active:t.integrationName===n?.integrationName,integration:t,icon:(0,e8.fK)(t.integrationName),onClick:()=>e.onSelectIntegration(t)},t.id))})},{}),(0,r.jsx)(()=>e.integrations.getBy(e.teamId,{filterBy:"dataPushIssueTracker",sortBy:"standard"}).filter(t=>!e.excludeInternalIntegrations||!t.internal).filter(t=>!e.excludeEmailIntegration||"email"!==t.integrationName).filter(e=>"intercom"!==e.integrationName).filter(e=>!t||e.userConfigured).map(t=>(0,r.jsx)(ty,{active:t.integrationName===n?.integrationName,integration:t,icon:(0,e8.fK)(t.integrationName),onClick:()=>e.onSelectIntegration(t)},t.id)),{}),t?(0,r.jsx)(tA,{onClick:e.onConnectMoreApps,icon:(0,r.jsx)(tx.v,{}),appearance:"dark",textType:"body",children:"Connect more apps"}):null]})}),tA=(0,i.Z)(es.z)`
  justify-content: flex-end;
  padding: 8px 16px;
  border-radius: 0;
  border: none;
  line-height: 1;
  color: ${ei.O.darkGrey};

  svg {
    color: ${ei.O.darkGrey} !important;
    margin-right: 12px;
    width: 20px;
  }

  span {
    font-size: ${tm.C.bodyMedium};
    font-weight: ${ea.v.regular};
  }

  &:hover,
  &:focus {
    background: ${ei.O.nearBlack};
    border-color: ${ei.O.charcoalGrey};
    span,
    svg {
      color: ${ei.O.darkGrey} !important;
    }
  }
`;var tN=n(14269),tT=n(97784);function tR(e){let t=e.src??void 0;t?.includes("avatars.jam.dev")&&(t=void 0);let n=e.firstLetter.toUpperCase(),i=e.borderRadius??"6px",a=e.size??24,o=tP[n]??"lime",s=tZ(o),l=tD(o);return(0,r.jsxs)(tz,{size:a,children:[(0,r.jsx)(tM,{src:t,alt:n,radius:i}),(0,r.jsx)(tL,{radius:i,size:a,style:{backgroundColor:s,color:l},children:n})]})}let tz=(0,i.Z)(tN.fC)`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  overflow: hidden;
  user-select: none;
  width: ${e=>e.size}px;
  height: ${e=>e.size}px;
  flex-shrink: 0;
`,tM=(0,i.Z)(tN.Ee)`
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: ${e=>e.radius};
`,tL=(0,i.Z)(tN.NY)`
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  line-height: 1;
  font-size: 14px;
  font-weight: 500;
  border-radius: ${e=>e.radius};
  text-transform: uppercase;
`,tP={A:"blue",B:"amber",C:"lime",D:"amber",E:"crimson",F:"blue",G:"cyan",H:"blue",I:"amber",J:"lime",K:"amber",L:"crimson",M:"blue",N:"cyan",O:"blue",P:"amber",Q:"lime",R:"amber",S:"crimson",T:"blue",U:"cyan",V:"blue",W:"amber",X:"lime",Y:"amber",Z:"crimson"},tZ=e=>{switch(e){case"blue":return tT.iNS.blue3;case"amber":return tT.DzF.amber3;case"lime":return tT.LRo.lime3;case"crimson":return tT.WlT.crimson3;case"cyan":return tT.sl2.cyan3}},tD=e=>{switch(e){case"blue":return tT.iNS.blue11;case"amber":return tT.DzF.amber11;case"lime":return tT.LRo.lime11;case"crimson":return tT.WlT.crimson11;case"cyan":return tT.sl2.cyan11}};var tO=n(55607);function tE(e){let t=t=>{e.onSelectTeam(t),e.onClose()};return(0,r.jsxs)(tu,{children:[(0,r.jsx)(tU,{children:(0,r.jsx)(el.x,{color:"darkGrey",as:"span",size:"bodyMedium",weight:"medium",children:"Save to"})}),(0,r.jsx)(tg,{}),e.normalTeams?.length?(0,r.jsx)(tW,{children:e.normalTeams?.map(n=>r.jsx(tF,{onClick:t,selectedTeamId:e.selectedTeam?.id??null,team:n,avatar:n.logo},n.id))}):null]})}let tF=e=>(0,r.jsxs)(tp,{onClick:()=>e.onClick(e.team.id),children:[(0,r.jsx)(tR,{firstLetter:e.team.name.charAt(0),src:e.avatar}),(0,r.jsx)(el.x,{color:"white",truncate:!0,as:"span",weight:"medium",size:"bodyMedium",children:e.team.name}),e.selectedTeamId===e.team.id&&(0,r.jsx)(tv.J,{color:ei.O.white})]},e.team.id),tU=i.Z.div`
  height: 32px;
  align-items: center;
  display: flex;
  padding: 8px 16px;
`,tW=i.Z.div`
  display: flex;
  flex-direction: column;
  max-height: 320px;
  flex-direction: column;
  overflow-y: auto;

  ${tO.zl};
`,tB=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)(null),[i,a]=(0,u.useState)(!1),o=()=>{a(!1)};return(0,r.jsxs)("div",{children:[(0,r.jsx)("div",{ref:n,children:(0,r.jsxs)(tc,{onClick:()=>a(!0),children:[(0,r.jsx)(tR,{firstLetter:e.selectedTeam.name.charAt(0),src:e.selectedTeam.logo??void 0}),(0,r.jsx)(e7._,{color:ei.O.charcoalGrey})]})}),(0,r.jsx)(td.J,{isOpen:i,anchorEl:t,onClose:o,disableAutoFocus:!0,borderRadius:12,anchorOrigin:{vertical:"bottom",horizontal:"right"},transformOrigin:{vertical:-4,horizontal:"right"},children:(0,r.jsx)(tE,{onClose:o,selectedTeam:e.selectedTeam,onSelectTeam:t=>{o(),e.onSelectTeam(t)},normalTeams:e.normalTeams,userAvatar:e.userAvatar})})]})}),tG=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)(null),[i,a]=(0,u.useState)(!1),{onOpen:o,waitingForAuth:s,...l}=e,{selectedIntegration:d}=e.integrations;(0,u.useEffect)(()=>{if(e.autoSelectNextActiveIntegration&&d&&!d?.userConfigured){let t=e.integrations.sortedAvailableIntegrations(e.team.id).find(e=>e.userConfigured&&e.teamConfigured);e.integrations.selectIntegration(t)}},[e.team.id,e.autoSelectNextActiveIntegration,e.integrations,d]);let c=()=>{e.onClose?.(),a(!1)};return(0,r.jsxs)(r.Fragment,{children:[e.headless?null:(0,r.jsxs)(t_,{children:[(0,r.jsx)(tq,{size:"bodyMedium",weight:"medium",color:"newGrey",children:"Create a"}),(0,r.jsxs)(tV,{children:[(0,r.jsx)(tK,{ref:n,children:(0,r.jsx)(tH,{integrations:e.integrations,onOpen:()=>{a(!0),o?.()}})}),(e.normalTeams??[]).length>0&&(0,r.jsx)(tB,{selectedTeam:e.team,normalTeams:e.normalTeams,onSelectTeam:e.onSelectTeam,userAvatar:e.userAvatar})]})]}),(0,r.jsx)(td.J,{isOpen:e.headless?.open??i,anchorEl:e.headless?.anchor??t,onClose:c,disableAutoFocus:!0,container:e.headless?.anchor??t,borderRadius:12,anchorOrigin:{vertical:"bottom",horizontal:"left"},transformOrigin:{vertical:-4,horizontal:0},children:(0,r.jsx)(tu,{children:(0,r.jsx)(tJ,{...l,excludeEmailIntegration:!!e.headless,excludeLinkOption:!!e.headless,onSelectIntegration:e=>{c(),l.onSelectIntegration(e)},onClearSelectedIntegration:()=>{c(),l.onClearSelectedIntegration()},isLoading:e.isLoading&&!s})})})]})}),tJ=(0,c.Pi)(e=>{let{isLoading:t,...n}=e;return t?(0,r.jsx)("div",{children:(0,r.jsx)(ts,{})}):(0,r.jsx)(tI,{...n})}),tH=e=>{let t=e.integrations.selectedIntegration;return(0,r.jsxs)(tY,{onClick:e.onOpen,children:[void 0===t?(0,r.jsx)(e9,{}):e8.Y6(t.integrationName),(0,r.jsx)(el.x,{as:"span",truncate:!0,size:"bodyMedium",weight:"regular",children:(()=>{if(!t)return"Link to share";let e=(0,e4._g)(t.integrationName??"");return`${t.displayName} ${e}`})()}),(0,r.jsx)(tr,{grow:1,justify:"end",children:(0,r.jsx)(e7._,{color:ei.O.charcoalGrey})})]})},t_=i.Z.div`
  display: flex;
  align-items: center;
  gap: ${eo.W.SP200};
  min-width: 0;

  ${ew.w.tablet} {
    margin-bottom: 8px;
  }
`,tV=i.Z.div`
  display: grid;
  grid-template-columns: 1fr auto;
  gap: ${eo.W.SP200};
  min-width: 0;
  flex-grow: 1;

  /* if user has only one team, let select button take full width */
  &:has(> :only-child) {
    grid-template-columns: 1fr;
  }
`,tY=i.Z.button`
  display: flex;
  align-items: center;
  border-radius: ${eo.W.SP200};
  padding: ${eo.W.SP200} ${eo.W.SP300};
  gap: ${eo.W.SP200};
  width: 100%;
  background: ${ei.O.white};
  border: 1px solid ${ei.O.mediumGrey};
  box-shadow: ${eP.SHADOW1};

  svg {
    flex: none;
  }

  svg:first-of-type {
    width: 20px;
    height: 20px;
  }
`,tq=(0,i.Z)(el.x)`
  white-space: nowrap;
`,tK=i.Z.div`
  display: flex;
  flex: 1;
  min-width: 0;
`;var tQ=n(44496);function tX(e){let t=(0,r.jsx)(t2,{children:(0,r.jsxs)(tr,{dir:"column",gap:"SP250",children:[(0,r.jsxs)(el.x,{weight:"medium",size:"bodySmall",color:"white",children:["Now that your trial for workspace"," ",(0,r.jsx)("strong",{children:e.workspaceName})," has ended, new Jams you create will be visible to anyone with the link"]}),(0,r.jsxs)(tr,{justify:"space-between",children:[(0,r.jsx)(t1,{variant:"primary",onClick:e.onUpgradePlansClick,children:"Upgrade plans"}),(0,r.jsx)(t1,{variant:"secondary",onClick:e.onClose,children:"Dismiss"})]})]})});return(0,r.jsx)(tw.u,{open:e.open,placement:"bottom-start",title:t,disablePortal:!0,interactive:!0,children:e.children})}let t0=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)(!1),i=(0,g.fe)(),a=(0,g.$7)(),o=(0,g.MU)(),s=(0,tQ.J)(o),l=i.filterByVariant("BusinessTrialEndedDashboard",a.selectedTeamId),d=l.length>0&&"teamId"in l[0]?l[0].teamId:"",c=a.teams?.find(e=>e.id===d)?.name??"unknown",p=(0,u.useRef)(new Set),m=(0,u.useRef)(new Set),x=(0,u.useCallback)(()=>{n(l.length>0),!(l.length>0)||l[0].deactivatedAt||p.current.has(l[0].id)||(s.viewInAppNotification({id:l[0].id}),p.current.add(l[0].id))},[s,JSON.stringify(l)]),h=(0,u.useCallback)(()=>{t&&(n(l.length>0),!(l.length>0)||l[0].deactivatedAt||m.current.has(l[0].id)||(s.deactivateInAppNotification({id:l[0].id}),m.current.add(l[0].id)))},[s,JSON.stringify(l)]);(0,u.useEffect)(()=>{x()},[x]);let f=(0,u.useCallback)(()=>{l.length>0&&(eS(d,j.AN.Unknown,{[I.t1.SOURCE]:"extension:iframe",[I.t1.CONTENT]:"business-trial-end"}),h())},[JSON.stringify(l)]);return(0,r.jsx)(tX,{workspaceName:c,open:t,onClose:h,onUpgradePlansClick:f,children:e.children})}),t1=i.Z.a`
  font-weight: ${ea.v.medium};
  font-size: ${tm.C.bodySmall};

  &:hover {
    text-decoration: none;
  }

  ${e=>"primary"===e.variant?(0,te.iv)`
        color: ${ei.O.blueberry};
        &:hover {
          color: ${ei.O.lightBlueberry};
        }
      `:(0,te.iv)`
        color: ${ei.O.darkGrey};
        &:hover {
          color: ${ei.O.mediumGrey};
        }
      `}
`,t2=i.Z.div`
  max-width: 326px;
  text-wrap: wrap;
  padding: 5px 0;
`,t5=(0,c.Pi)(e=>{let{user:t}=(0,g.dR)(),{integrationsStore:n,authStore:i}=e,o=e.authStore.selectedTeamId,s=t?.teams.find(e=>e.id===o),d=(0,u.useRef)(!1);if((0,u.useEffect)(()=>{!n.availableIntegrationsLoading&&d.current&&((0,l.Y)().finalize("integrations_render_list","success"),d.current=!1)},[n.availableIntegrationsLoading]),!s)return null;async function c(e){i.setSelectedTeamId(e),n.setTeamId(e),n.setSelectedIntegration(e,void 0);let t=n.syncedDataStore?.getSelectedIntegration(e);t&&(await n.onIntegrationChange(t),n.syncContextDown())}return(0,r.jsx)(t6,{children:(0,r.jsx)(t0,{children:(0,r.jsx)(tG,{onOpen:()=>{let e=(0,l.Y)();n.availableIntegrationsLoading?(e.create("integrations_render_list",{createTimeout:a.eq("1s"),traceTimeout:a.eq("10s")}),d.current=!0):(0,l.Y)().create("integrations_render_list",{mode:"insert-finalized",state:{type:"finalized",variant:"success",createdAt:Date.now(),finalizedAt:Date.now()}})},userAvatar:i.me.data?.avatarSrc,autoSelectNextActiveIntegration:!0,normalTeams:i.normalTeams,onSelectTeam:c,excludeInternalIntegrations:!1,integrations:n,teamId:s.id,team:s,teamEntitlements:e.myFeaturesStore,waitingForAuth:e.waitingForAuth,isLoading:n.availableIntegrationsLoading,onSelectIntegration:async t=>{t.userConfigured&&t.teamConfigured||e.setWaitingForAuth(t.integrationName),await n.onIntegrationChange(t.integrationName),n.syncContextDown(),n.syncSelectedTeamIntegrationUp()},onClearSelectedIntegration:()=>{n.clearSelectedIntegration(),n.syncSelectedTeamIntegrationUp()},onConnectMoreApps:()=>{window.open(`${eC.v.DASH_URL}/s/${s.id}/settings/connected-apps?${I.I4.CONNECT_MORE_APPS}=true`,"_blank")}})})})}),t6=i.Z.section`
  padding: 24px;
  border-top-right-radius: 16px;
  align-items: baseline;
  min-height: 68px;
  gap: 24px;
  overflow: visible;
`,t3={description:null,dismissed:!1,generationId:null,sessionId:null,status:"idle",title:null};async function t4(e,t,n){let r=(0,$.Z)(),i=await e.send({eventName:"GetAiSummary",dest:{component:s.wA.Main,location:void 0},data:{aiSessionId:n,localGenerationId:r,tabId:t.tabId,teamId:t.teamId,trigger:"mount"},timeout:a.eq("30s")});return i.ok?{description:i.value.description,dismissed:!1,generationId:i.value.generationId,sessionId:n,status:"ready",title:i.value.title}:{description:null,dismissed:!1,generationId:null,sessionId:n,status:"error",title:null}}function t7(e){return`${e.teamId}:${e.tabId}`}function t9(e){return{description:e.description,dismissed:e.dismissed,generationId:e.generationId,sessionId:e.sessionId,status:e.status,title:e.title}}function t8(e,t,n){let r=function(e){var t;let{state:n,hasTitle:r,ghostVisible:i,hasAcceptedContent:a}=e;if("error"===n.status)return i?{kind:"clear"}:{kind:"none"};if(n.dismissed||"idle"===n.status||a)return{kind:"none"};if("loading"===n.status)return{kind:"loading"};let o=(t=n,r&&t.title?`### ${t.title}

${t.description??""}`:t.description??null);return o?{kind:"suggest",text:o}:{kind:"none"}}({state:t,hasTitle:n,ghostVisible:"disabled"!==(0,V.yt)(e),hasAcceptedContent:null!==ne(e)});switch(r.kind){case"clear":e.commands.clearSuggestion();break;case"loading":e.commands.setSuggestion(n?"### Add a title or wait for AI\n\nWrite a description or @ to mention":"Write a description or wait for AI",{showSpinner:!0});break;case"suggest":e.commands.setSuggestion(r.text,{showSpinner:!1})}}function ne(e){return"disabled"!==(0,V.yt)(e)||0===e.getText().trim().length?null:e.getJSON()}function nt(e,t){return!e||e.type!==ej.Wz.None&&(e.type!==ej.Wz.Restricted||e.value.includes(t))}let nn=(0,c.Pi)(e=>{let{integrationsStore:t,inAppNotificationsStore:n,foldersStore:i,newThreadStore:o,authStore:l,globallySyncedStore:d}=e,{capture:c,teamFeatureUsage:p}=d,x=(0,u.useRef)(null),h=(0,u.useRef)(null),v=(0,g.MU)(),w=(0,g.z3)(),y=(0,m.i)();async function C(e){let n=t.getFileTypes(),{accepted:r,rejectedSizeCount:i,rejectedTypeCount:s,rejectedOverflowCount:l}=function(e,t){let{isTypeAllowed:n}=t,r=n?e.filter(e=>n(e.type)):e,i=e.length-r.length,a=r.filter(e=>e.size<=5e6),o=r.length-a.length,s=Math.max(0,t.maxFiles-t.currentCount),l=a.slice(0,s),d=a.length-l.length;return{accepted:l,rejectedSizeCount:o,rejectedTypeCount:i,rejectedOverflowCount:d}}(e,{currentCount:o.attachments.length,maxFiles:5,isTypeAllowed:e=>nt(n,e)});l>0&&y({title:"You can attach up to 5 files",ttl:a.eq("3s"),dismissable:!0}),s>0&&y({title:`${s} unsupported ${eI()("file",s)}`,ttl:a.eq("3s"),dismissable:!0}),i>0&&y({title:`${i} ${eI()("file",i)} over the 5 MB limit`,ttl:a.eq("3s"),dismissable:!0}),0!==r.length&&o.addAttachments(await Promise.all(r.map(A)))}let S=(0,u.useRef)(C);S.current=C;let M=(0,u.useMemo)(()=>{var e;return e=e=>S.current(e),W.hj.create({name:"fileDrop",addProseMirrorPlugins(){let t=null,n=()=>{t&&(clearTimeout(t),t=null)},r=(e,t)=>{e.dom.classList.toggle("file-drop-active",t),t?e.dom.dataset.fileDropPlaceholder="Drop your files here":(delete e.dom.dataset.fileDropPlaceholder,e.dom.classList.remove(G))},i=(e,t)=>{let n=t.target;r(e,!0),e.dom.classList.toggle(G,n instanceof Node&&e.dom.contains(n))},a=e=>{n(),r(e,!1)},o=e=>{n(),t=setTimeout(()=>r(e,!1),100)};return[new B.Sy({props:{handleDOMEvents:{dragover:(e,t)=>!!J(t)&&(t.preventDefault(),!0),dragend:e=>(a(e),!1)},handleDrop:(t,n)=>{a(t);let r=Array.from(n.dataTransfer?.files??[]);return 0!==r.length&&(n.preventDefault(),e(r),!0)},handlePaste:(t,n)=>{let r=Array.from(n.clipboardData?.files??[]);return 0!==r.length&&(n.preventDefault(),e(r),!0)}},view(e){let t=e.dom.ownerDocument,r=t.defaultView,s=()=>a(e),l=t=>{J(t)&&(n(),i(e,t))},d=n=>{if(!J(n))return;let r=n.relatedTarget;!(r instanceof Node&&t.documentElement.contains(r))&&o(e)};return t.addEventListener("dragenter",l,!0),t.addEventListener("dragover",l,!0),t.addEventListener("dragleave",d,!0),t.addEventListener("drop",s,!0),t.addEventListener("dragend",s,!0),r?.addEventListener("blur",s),{destroy(){a(e),t.removeEventListener("dragenter",l,!0),t.removeEventListener("dragover",l,!0),t.removeEventListener("dragleave",d,!0),t.removeEventListener("drop",s,!0),t.removeEventListener("dragend",s,!0),r?.removeEventListener("blur",s)}}}})]}})},[]),L=l.selectedTeamId,P=l.me?.data?.id,D=!t.syncedDataStore.loaded||!t.selectedIntegration||t.displayFields.has("title"),{mentionSuggestion:O}=function(e){let t=(0,g.$7)(),n=t.data?.id,i=t.data?.teams.find(t=>t.id===e)?.members,a=i?(0,eM.vM)(i):void 0,{mentionSuggestion:o}=function(e){let{members:t,resolveMember:n}=e,i=(0,u.useRef)(t);i.current=t;let a=(0,u.useRef)(n);return a.current=n,{mentionSuggestion:(0,u.useMemo)(()=>{var e;return e={membersRef:i,resolverRef:a},{buildExtension:t=>eN.Z.configure({hasResolver:()=>null!=e.resolverRef.current,resolveMember:t=>e.resolverRef.current?.(t)??null,suggestion:{char:"@",...t,allow:({state:e,range:t})=>"heading"!==e.doc.resolve(t.from).parent.type.name,command:({editor:e,range:t,props:n})=>(function({editor:e,range:t,member:n}){e.chain().focus().insertContentAt(t,[{type:"mention",attrs:{targetType:"user",targetId:n.id,label:n.name}},{type:"text",text:" "}]).run(),window.getSelection()?.collapseToEnd()})({editor:e,range:t,member:n})}}),getItemKey:e=>e.id,getSelectedValue:e=>e,id:"jamMentionSuggestion",items:({query:t})=>(function(e,t){let n=t.toLowerCase();return(n?e.filter(e=>e.displayName.toLowerCase().includes(n)||e.name.toLowerCase().includes(n)||(e.email?.toLowerCase().includes(n)??!1)):e).slice(0,10)})(e.membersRef.current,t),pluginKey:eT,renderItem:({item:e})=>(0,r.jsxs)(u.Fragment,{children:[(0,r.jsx)(eR,{src:e.avatarSrc??void 0,fallback:e.displayName.charAt(0),size:"1",radius:"full"}),(0,r.jsx)(ez,{as:"span",truncate:!0,children:e.displayName})]})}},[])}}({members:(0,u.useMemo)(()=>{var e;return(e=function(e,t){if(!e)return e;let n=null==t?[...e]:e.filter(e=>e.id!==t);return n.sort((e,t)=>{let n=eL(e.lastActiveAt),r=eL(t.lastActiveAt);return n!==r?r-n:e$(e).localeCompare(e$(t))}),n}(a,n))?e.map(e=>({id:e.id,displayName:e$(e),name:e$(e),email:e.email,avatarSrc:e.avatarSrc})):[]},[a,n]),resolveMember:(0,u.useMemo)(()=>(function(e){if(e)return t=>{let n=e.find(e=>e.id===t);return n?{name:e$(n),email:n.email,avatarSrc:n.avatarSrc}:null}})(a),[a])});return{mentionSuggestion:o}}(L),{emojiSuggestion:E}=(0,H.I)(),F=(0,u.useMemo)(()=>{let e=[e_,Y.configure({forceFocusDelay:200}),M];return D&&e.push(K.Eq),e},[D,M]),U=(0,u.useMemo)(()=>[O,E],[O,E]),_=d.isTeamAiSummaryEnabled(L),q=d.isAiSummaryEnabled,{updateUserPreferences:en}=function(){let e=(0,g.MU)();return{updateUserPreferences:async t=>{await e.send({eventName:"UpdateUserPreferences",dest:{component:s.wA.Main},data:{preferences:t}})}}}();(function(e){let t=(0,g.MU)(),{teamId:n,globallySyncedStore:r,foldersStore:i}=e;(0,u.useEffect)(()=>{async function e(){await b(t,i,n),r.lastSelected?.folderId&&i.selectFolderById(r.lastSelected.folderId)}i.isLoading||e()},[e.teamId])})({globallySyncedStore:d,authStore:l,foldersStore:i,teamId:L}),function(e){let t=(0,g.MU)(),{userId:n,inAppNotificationsStore:r}=e;(0,u.useEffect)(()=>{async function e(){if(!n)return;r.setLoading(!0);let e=await t.send({eventName:"GetInAppNotifications",data:null,dest:{component:s.wA.Main,location:void 0}}).finally(()=>r.setLoading(!1));r.update(e)}r.loading||e()},[n,t,r])}({userId:P,inAppNotificationsStore:n});let er=(0,g.EO)(),{hasReachedLimit:ei}=k(),ea=_&&q&&!ei,[eo,es]=function(e){let[t,n]=(0,u.useState)(null),r=e.getIntegration(t??"");return(0,u.useEffect)(()=>{if(t&&r)return(0,f.U5)(()=>r.userConfigured,t=>{t&&(e.selectIntegration(r),n(null))})},[t,e,r]),[t,n]}(t),el=er.screenshot.screenshotIsCaptured&&null===er.screenshot.compositeScreenshot,ed=t.isLoadingIntegrationFields||"pre_draft"===c.state.name||"submission"===c.state.name||el,ec=c.type===ej.K8.Video&&("pre_draft"===c.state.name||"draft"===c.state.name)?c.state.payload.toolsSummary:null,[eu,ep]=(0,u.useState)(null),[eg,em]=(0,u.useState)(!1),ex=e=>{if(o.setContentSnapshot(e),D){let n=(e.content?.[0]?.content??[]).map(e=>e.text??"").join("");t.setFieldValue("title",n)}},eh=function(e){let t=(0,u.useRef)(null);t.current||(t.current=function(){let e=new Map;return{dismiss:t=>{let n=t7(t),r=e.get(n);r&&e.set(n,{...r,dismissed:!0})},get:t=>{if(!t.enabled)return{state:t3};let n=t7(t.params),r=e.get(n);if(r)return{promise:r.promise,state:t9(r)};let i=(0,$.Z)(),a=t4(t.broker,t.params,i).then(t=>{let r=e.get(n),i=r?.dismissed?{...t,dismissed:!0}:t;return e.set(n,i),t9(i)}).catch(()=>{let t=e.get(n),r={...t3,dismissed:t?.dismissed??!1,sessionId:i,status:"error"};return e.set(n,r),t9(r)}),o={...t3,promise:a,sessionId:i,status:"loading"};return e.set(n,o),{promise:a,state:t9(o)}},getAcceptedIds:t=>{let n=t7(t),r=e.get(n);return r?.sessionId&&r?.generationId?{sessionId:r.sessionId,generationId:r.generationId}:null}}}());let n=(0,g.rC)(),{editor:r,query:i}=e,{hasTitle:a,onAcceptedContent:o}=r,{params:l}=i;return{onCreate:e=>{let r=t.current?.get(i);r&&(r.state.sessionId&&n.setSessionId(r.state.sessionId),t8(e,r.state,a),r.promise?.then(t=>{t.sessionId&&n.setSessionId(t.sessionId),e.isDestroyed||t8(e,t,a)}),e.on("transaction",({transaction:n})=>{n.getMeta("acceptSuggestion")&&(o(e.getJSON()),t.current?.dismiss(l),function(e,t,n){let r=n?.getAcceptedIds(t);r&&e.send({eventName:"NotifyAiGenerationAccepted",dest:{component:s.wA.Main,location:void 0},data:{aiSessionId:r.sessionId,aiGenerationId:r.generationId}})}(i.broker,l,t.current))}))},onUnmount:e=>{let n=null!==ne(e);((0,V.tZ)(e)||n)&&t.current?.dismiss(l),n&&o(e.getJSON())}}}({editor:{hasTitle:D,onAcceptedContent:ex},query:{broker:v,enabled:ea&&c.type===ej.K8.Video,params:{tabId:w,teamId:L}}});if(!d.user?.teams.find(e=>e.id===L))return null;let ef=d.myFeatures,eb=ec?function(e,t){let n=[];switch((e?.blur.numBlurredSelectors??-1)>0&&!t.hasAccess(j.AN.CaptureScreenRecordingBlur,"any")&&0>=t.numDemoUsesRemaining(j.AN.CaptureScreenRecordingBlur)&&n.push("blur"),e?.annotations.didUseAnnotations&&!t.hasAccess(j.AN.CaptureScreenRecordingAnnotations,"any")&&0>=t.numDemoUsesRemaining(j.AN.CaptureScreenRecordingAnnotations)&&n.push("annotations"),n.length){case 0:return;case 1:return`Please upgrade to use the ${n[0]} feature`;case 2:return`Please upgrade to use the ${n.join(" and ")} features`;default:return"Please upgrade to use these features"}}(ec,ef):void 0,ev="draft"===c.state.name&&c.state.payload.resumedDraft,ew=t.getFileTypes(),ey=o.attachments.filter(e=>nt(ew,e.type)).map(e=>({id:e.id,name:e.name,type:e.type,src:e.source}));return(0,r.jsx)(ni,{"data-testid":"comment-modal",children:(0,r.jsxs)(na,{ref:ep,children:[(0,r.jsxs)(no,{children:[(0,r.jsx)(eO,{closeJam:e.closeJam,resumedDraft:ev}),e.children]}),(0,r.jsx)(ns,{children:(0,r.jsxs)(nl,{children:[(0,r.jsx)(ee.v,{integrations:t}),(0,r.jsx)(t5,{authStore:e.authStore,myFeaturesStore:ef,integrationsStore:t,waitingForAuth:eo,setWaitingForAuth:es}),(0,r.jsx)(nd,{children:(0,r.jsx)(Q.H4,{ref:x,content:(0,K.DE)(o.getMessageContent(),D),onChange:ex,onCreate:eh.onCreate,onUnmount:eh.onUnmount,onSubmit:e.handleCreateThread,extensions:F,suggestions:U,suggestionSide:"bottom"},`${String(D)}:${String(ea)}`)}),(0,r.jsx)(N.k,{px:"3",children:(0,r.jsx)(Z,{attachments:ey,onRemove:o.removeAttachment})}),(0,r.jsx)(et.V,{tooltipContainer:eu,integrations:t}),(0,r.jsx)(nc,{children:(0,r.jsx)(nr,{teamId:L,onUpgrade:e=>eS(L,e,{[I.t1.SOURCE]:"extension:iframe",[I.t1.CONTENT]:"draft-modal-banner"}),toolsSummary:ec,myFeatures:ef,shouldShowAiGenerationBanner:ea,teamFeatureUsage:p})}),(0,r.jsx)("input",{ref:h,type:"file",multiple:!0,hidden:!0,onChange:e=>{let t=Array.from(e.target.files??[]);t.length>0&&C(t),e.target.value=""}}),(0,r.jsxs)(N.k,{minWidth:"0",p:"4",children:[(0,r.jsxs)(N.k,{flexGrow:"1",minWidth:"0",align:"center",gap:"2",pr:"3",children:[ew?.type!==ej.Wz.None&&(0,r.jsx)(T.u,{content:"Attach files",children:(0,r.jsx)(R.h,{size:"1",variant:"ghost",color:"gray",onClick:()=>h.current?.click(),children:(0,r.jsx)(X,{size:16})})}),(0,r.jsx)(e6,{foldersStore:i}),_&&c.type===ej.K8.Video&&(0,r.jsx)(eq,{enabled:q&&!ei,locked:ei,lockedReason:"You've reached your Jam quota. AI is locked until your quota resets.",onChange:e=>en({aiSummaryEnabled:e})})]}),(0,r.jsx)(T.u,{content:eb??"",hidden:!eb,children:(0,r.jsx)(z.z,{loading:eg,onClick:async()=>{if(ei){e.closeJam({showToast:!0,storeDraft:!0});return}em(!0);try{await e.handleCreateThread()}finally{em(!1)}},disabled:eg||ed||!!eb,children:ei?"Save to drafts":"Create"})})]})]})})]})})}),nr=(0,c.Pi)(e=>{let{onUpgrade:t,toolsSummary:n,myFeatures:i,shouldShowAiGenerationBanner:a,teamId:o}=e,s=e.teamFeatureUsage.get(o,j.AN.TeamJamQuotaLimit);return s&&s.limit>-1?(0,r.jsx)(ed,{feature:j.AN.TeamJamQuotaLimit,shouldShow:()=>s.remaining<=5,onUpgrade:t,text:()=>`${s.current}/${s.limit} ${eI()("Jam",s.limit)} created this month`,isDismissable:()=>s.remaining>0}):(n?.blur.numBlurredSelectors??-1)>0&&!i.hasAccess(j.AN.CaptureScreenRecordingBlur,"any")&&0>=i.numDemoUsesRemaining(j.AN.CaptureScreenRecordingBlur)?(d.k.warn("Showing special-case `0 demo uses remaining` banner",{featureName:"blur"}),(0,r.jsx)(ex,{feature:j.AN.CaptureScreenRecordingBlur,store:i,onUpgrade:t,text:(e,t)=>`${e}/${t} ${eI()("video blur",t)} left`})):n?.annotations.didUseAnnotations&&!i.hasAccess(j.AN.CaptureScreenRecordingAnnotations,"any")&&0>=i.numDemoUsesRemaining(j.AN.CaptureScreenRecordingAnnotations)?(d.k.warn("Showing special-case `0 demo uses remaining` banner",{featureName:"annotations"}),(0,r.jsx)(ex,{feature:j.AN.CaptureScreenRecordingAnnotations,store:i,onUpgrade:t,text:(e,t)=>`${e}/${t} ${eI()("video annotation",t)} left`})):a?(0,r.jsx)(ex,{dismissable:!0,feature:j.AN.AiSummaryGeneration,store:i,onUpgrade:t,text:(e,t)=>`${e}/${t} ${eI()("AI summary",t)} left`}):null}),ni=i.Z.div`
  padding: 24px;
  max-width: 100%;
  max-height: 100%;
  min-height: 340px;

  width: 90%;
  height: 90%;
  ${ew.w.mobile} {
    padding: 0;
  }
`,na=i.Z.div`
  display: flex;
  width: 100%;
  height: 100%;

  ${ew.w.tablet} {
    flex-direction: column;
  }

  box-shadow: 0px 4px 32px rgba(0, 0, 0, 0.2);
  border-radius: 16px;
`,no=i.Z.div`
  padding: ${eo.W.SP600};
  display: flex;
  flex-direction: column;
  background: ${ei.O.lightGrey};
  border-top-left-radius: 16px;
  border-bottom-left-radius: 16px;
  position: relative;
  z-index: 1;
  min-width: 0; // fix flex overflow
  flex: 1;
  justify-content: center;
  ${ew.w.tablet} {
    border-radius: 16px 16px 0 0;
  }
`,ns=i.Z.div`
  display: flex;
  position: relative;
  background: ${ei.O.white};
  width: 372px;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;

  ${ew.w.tablet} {
    width: auto;
    border-radius: 0 0 16px 16px;
    overflow: auto;
  }
`,nl=i.Z.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;

  ${ew.w.tablet} {
    height: max-content;
  }
`,nd=i.Z.div`
  padding: 0 12px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: auto;

  .editor-root,
  .editor-content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;

    .tiptap {
      flex-grow: 1;
    }
  }

  .ghost-text-loader {
    display: inline-flex;
    padding-left: 4px;
  }

  .ghost-text-content {
    color: rgba(0, 0, 0, 0.32);
  }

  h3.ghost-text-content .ghost-text-loader {
    transform: translateY(-5px);
  }

  p.ghost-text-content .ghost-text-loader {
    transform: translateY(-3px);
  }

  .ghost-text-accept {
    display: block;
  }
`,nc=i.Z.div`
  padding: 0 20px 20px 20px;

  &:empty {
    display: none;
  }
`;async function nu(e){let{broker:t,integrationsStore:n,globallySyncedStore:r}=e,i=r.currentTab.id,o=function(e){if(e.hasSelectedIntegration()){let t=e.invalidFieldValues,n=e.selectedIntegration?.displayName;if(t)return{title:`Some ${n} values are invalid.`,description:t.map(e=>e.message).join(", "),icon:"warning",ttl:a.eq("3s")};if(e.displayFieldsLoading)return{title:`${n} fields are currently loading, please wait.`,icon:"warning",ttl:a.eq("2s")}}}(n);if(o){(0,m.G)(t,i,o);return}n.storeRecentlyUsedFields();let s=n.hasSelectedIntegration()?n.onSubmitUserMessage:"Creating a link for you, on its way shortly!",{toastId:l}=await (0,m.G)(t,i,{title:s,ttl:a.eq("2m"),icon:"loading"});return{toastId:l}}let np=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)("idle"),i=(0,g.dR)(),c=(0,g.$7)(),f=(0,g.b3)(),b=(0,g.Pn)(),w=(0,g.fe)(),j=(0,g.__)(),k=(0,g.MU)(),I=function(e=x){let[t,n]=(0,u.useState)(void 0),r=(0,g.MU)(),[i,a]=(0,u.useState)(0),[o,l]=(0,u.useState)(),d=(0,g.dR)().currentTab.id,c=(0,m.i)();async function p(){l((await c({title:"Press esc again to close Jam",icon:"info"})).toastId)}return(0,u.useEffect)(()=>()=>{o&&r.send({eventName:"RemoveToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:d},data:{toastId:o}}),window.clearTimeout(t)},[t,o,r,d]),async function(){if(void 0===o&&await p(),Date.now()-i<e.gracePeriodMs){await r.send({eventName:"RemoveToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:d},data:{toastId:o}}),l(void 0),await r.send({eventName:"Dismiss",dest:{component:s.wA.Main,location:void 0},data:{}});return}a(Date.now()),n(window.setTimeout(()=>{r.send({eventName:"RemoveToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:d},data:{toastId:o}}),l(void 0)},e.gracePeriodMs))}}(),$=S();!function(e){let[t,n]=(0,u.useState)(!1),r=(0,g.MU)(),i=(0,g.rC)(),a=(0,g.b3)(),o=(0,g.__)(),l=(0,g.Pn)(),c=(0,g.$7)().selectedTeamId;(0,u.useEffect)(()=>{(async function(){if("draft"===e.state.name&&e.state.payload?.resumedDraft&&!t)try{d.k.info(`resuming ${e.type} draft`);let t=await r.send({eventName:"GetDraftResumableState",dest:{component:s.wA.Main,location:void 0},data:null});if(t.ok){let{message:n,aiSessionState:s,folderId:u,integrationState:p,attachments:g}=t.value;d.k.info(`resuming ${e.type} draft with data`,{message:!!n,aiSessionState:!!s,folderId:!!u,integrationState:!!p,attachments:!!g}),s?.sessionId&&v(()=>i.resumeSessionState(s),"restoring aiSessionState",{aiSessionState:s}),n&&v(()=>a.setInitialContentFromJSON(n),"restoring message",{message:n}),g&&v(()=>a.addAttachments(g),"restoring attachments",{teamId:c,attachmentCount:g?.length}),await Promise.all([C(r,o,c,u).catch(e=>{d.k.error("error on restoring folder",{error:(0,h.LT)(e),folderId:u,teamId:c})}),y(l,p,c).catch(e=>{d.k.error("error on restoring integration state",{error:(0,h.LT)(e),teamId:c,integrationName:p?.integrationName})})])}d.k.info(`resumed ${e.type} draft successfully`)}catch(e){d.k.error("failed to or resume part of the draft state",{error:(0,h.LT)(e),teamId:c})}finally{n(!0)}})()},[e,t,c,r,i,a,o,l])}(i.capture),(0,u.useEffect)(()=>()=>{k.send({eventName:"FreezeClickEvents",dest:{component:s.wA.HostScript,location:s.Ye.HostScripts.AdditionalHooks,tabId:i.currentTab.id},data:!1})},[k,i.currentTab.id]);let A=(0,u.useRef)(null);return"complete"===t?null:(0,r.jsx)(ng,{ref:A,submitState:t,children:(0,r.jsx)(o.V,{fullScreen:!0,open:!0,onClose:I,disablePortal:!0,borderRadius:32,backgroundColor:"transparent",children:(0,r.jsx)(nn,{globallySyncedStore:i,newThreadStore:f,integrationsStore:b,inAppNotificationsStore:w,foldersStore:j,authStore:c,handleCreateThread:async()=>{try{let e=await (0,l.Y)().create("jam_create",{createTimeout:a.eq("1s"),traceTimeout:a.eq("1m")});d.k.debug("jam_create trace result",{traceResult:e})}catch(e){d.k.error("jam_create trace error",{error:e})}try{$()}catch(e){d.k.warn("jam_create syncContextUp error",{error:e})}let t=await nu({broker:k,integrationsStore:b,globallySyncedStore:i});t&&(e.onBeforeSubmit&&((0,p.flushSync)(()=>{n("in-progress")}),await e.onBeforeSubmit()),await e.onSubmit(t),n("complete"))},closeJam:async(e={})=>{await k.send({eventName:"Dismiss",dest:{component:s.wA.Main,location:void 0},data:e})},children:e.children})})})}),ng=i.Z.div`
  position: relative;
  pointer-events: auto;
  padding: 32px;

  opacity: ${e=>"in-progress"===e.submitState||"complete"===e.submitState?0:1};
  transition: opacity 0.1s;
`},16140:function(e,t,n){n.d(t,{Z:()=>a});var r=n(63403),i=n(49710);async function a(e){let t=e.captureType===i.K8.Screenshot?"CreateJamScreenshot":e.captureType===i.K8.Video?"CreateJamVideo":"CreateJamReplay";return e.broker.send({eventName:t,dest:{component:r.wA.Main,location:void 0},data:e.data})}}};
//# sourceMappingURL=72.js.map