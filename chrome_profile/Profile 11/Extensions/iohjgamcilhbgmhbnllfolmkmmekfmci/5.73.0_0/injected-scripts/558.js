export const ids=["558"];export const modules={78213:function(e,t,n){n.d(t,{h:()=>l});var r=n(52322),i=n(7184),a=n(51749),o=n(2784);let s={solid:"solid",soft:"soft",ghost:"soft",surface:"surface",outline:"outline"},l=o.forwardRef((e,t)=>{let{variant:n="solid",...i}=e;return(0,r.jsx)(d,{ref:t,variant:s[n],"data-variant":n,...i})});l.displayName="IconButton";let d=(0,i.Z)(a.h)`
  border-radius: var(--radius-3);

  // ghost variant is "soft" under the hood, we just need to override the background here
  &[data-variant="ghost"] {
    background-color: transparent;

    &:hover:not(:disabled) {
      background-color: var(--gray-a3);
    }
  }
`},75818:function(e,t,n){n.d(t,{u:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M11.9998 9v4m0 4h.01M10.6151 3.8917l-8.225 14.2066c-.4561.788-.6842 1.182-.6505 1.5054.0294.282.1772.5383.4065.7051.263.1912.7182.1912 1.6288.1912h16.4497c.9106 0 1.3658 0 1.6288-.1912a1 1 0 0 0 .4065-.7051c.0337-.3234-.1944-.7174-.6506-1.5054L13.3844 3.8917c-.4545-.7852-.6818-1.1777-.9783-1.3096a1 1 0 0 0-.8126 0c-.2966.1319-.5239.5244-.9784 1.3096",vectorEffect:"non-scaling-stroke"})})},92622:function(e,t,n){n.d(t,{J:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M20 6 9 17l-5-5",vectorEffect:"non-scaling-stroke"})})},60351:function(e,t,n){n.d(t,{b:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M3 9h13.5c2.4853 0 4.5 2.0147 4.5 4.5S18.9853 18 16.5 18H12M3 9l4-4M3 9l4 4",vectorEffect:"non-scaling-stroke"})})},32016:function(e,t,n){n.d(t,{Y:()=>i});var r=n(52322);n(2784);let i=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M21 9H7.5C5.0147 9 3 11.0147 3 13.5S5.0147 18 7.5 18H12m9-9-4-4m4 4-4 4",vectorEffect:"non-scaling-stroke"})})},6891:function(e,t,n){n.d(t,{Q:()=>a});var r=n(2784),i=n(25171);function a(e){let{interaction:t,variant:n,tags:a,policy:o}=e,s="onMount"===o.when?[]:[o.condition],l=r.useRef(!1);r.useEffect(()=>{!l.current&&("onCondition"!==o.when||o.condition)&&(l.current=!0,"failure"===n?(0,i.Y)().finalize(t,"failure",{error:e.error,tags:a}):(0,i.Y)().finalize(t,n,{tags:a}))},s)}},29128:function(e,t,n){n.d(t,{Z:()=>nb});var r=n(52322),i=n(7184),a=n(82608),o=n(6648),s=n(63403),l=n(25171),d=n(70621),c=n(75958),u=n(2784),p=n(28316),g=n(28128),m=n(20322);let x={gracePeriodMs:2e3};var h=n(71509),f=n(80075);async function v(e,t,n){t.setTeamId(n),t.setIsLoading(!0);let r=await e.send({eventName:"GetFolders",data:{teamId:n},dest:{component:s.wA.Main,location:void 0}}).finally(()=>t.setIsLoading(!1));return r&&t.replaceFolders(r.map(e=>({id:e.id,name:e.name,teamId:e.teamId,lastChangedAt:new Date(e.lastChangedAt),quantity:e.quantity}))),t.availableFolders}function b(e,t,n){try{e()}catch(e){d.k.error(`error on ${t}`,{error:(0,h.LT)(e),...n})}}let w=(e,t=a.eq("10s"))=>new Promise((n,r)=>{if(!e.availableIntegrationsLoading){n();return}let i=setTimeout(()=>{a(),r(Error(`Timeout waiting for integrations to load after ${t}ms`))},t),a=(0,f.U5)(()=>e.availableIntegrationsLoading,e=>{e||(clearTimeout(i),a(),n())})});async function y(e,t,n){if(!t?.integrationName)return;await w(e);let r=e.getIntegration(t.integrationName,n);r&&(e.setSelectedIntegration(n,r),t.displayFieldsFilters&&Object.entries(t.displayFieldsFilters).forEach(([n,r])=>{n===t.integrationName&&e.setDisplayFieldsFilters(n,r)}),await e.fetchDisplayFieldsForSelectedIntegration(),Object.entries(t.fieldValues).forEach(([t,n])=>{e.displayFields.get(t)&&e.setFieldValue(t,n)}))}async function C(e,t,n,r){r&&((await v(e,t,n)).find(e=>e.id===r)?t.selectFolderById(r):d.k.warn("cannot resume selected folder, no avialable folder with id",{folderId:r}))}let j=()=>{let e=(0,g.Pn)(),t=(0,u.useCallback)(async()=>{e.syncSelectedTeamIntegrationDown(),await e.clearSelectedIntegrationContext(),e.syncContextDown()},[e]),n=(0,u.useCallback)(()=>{e.syncContextUp()},[e]);return(0,u.useEffect)(()=>{(async()=>{await e.syncedDataStore.fetchSyncedTeamIntegrationData(),t()})()},[e.syncedDataStore,t]),n};var S=n(33735);let k=()=>{let{teamFeatureUsage:e}=(0,g.dR)(),t=(0,g.$7)().selectedTeamId,n=e.get(t,S.AN.TeamJamQuotaLimit),r=!!(n&&n.limit>-1&&n.remaining<=5),i=!!(n&&n.limit>-1&&n.current>=n.limit);return{teamId:t,jamQuotaUsage:n,shouldShowWarning:r,hasReachedLimit:i}},I=RegExp("\\.(png|jpg|jpeg|gif|webp|heic|svg|mp4|webm|mov|mkv|avi|mp3|pdf|docx|xlsx|html|txt|csv|json|md|log|har|yaml|yml)$","i");RegExp("\\.(action|apk|app|bat|bin|cab|cmd|com|command|cpl|csh|ex_|exe|gadget|inf1|ins|inx|ipa|isu|job|jse|ksh|lnk|msc|msi|msp|mst|osx|out|paf|pif|prg|ps1|reg|rgs|run|scr|sct|shb|shs|u3p|vb|vbe|vbs|vbscript|workflow|ws|wsf)$","i");var $=n(76062),A=n(88767);async function T(e){let t=await new Promise((t,n)=>{let r=new FileReader;r.readAsDataURL(e),r.addEventListener("load",()=>{r.result&&t(r.result.toString())}),r.addEventListener("error",e=>{n(e)})});return{id:A.Z(),source:t,type:e.type,name:e.name,size:e.size}}var N=n(25016),R=n(27300),z=n(78213),M=n(87722),L=n(30199);let D=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M20 7v-.2c0-1.6802 0-2.5202-.327-3.162a3 3 0 0 0-1.311-1.311C17.7202 2 16.8802 2 15.2 2H8.8c-1.6802 0-2.5202 0-3.162.327a3 3 0 0 0-1.311 1.311C4 4.2798 4 5.1198 4 6.8v10.4c0 1.6802 0 2.5202.327 3.162a3 3 0 0 0 1.311 1.311C6.2798 22 7.1198 22 8.8 22h3.7m5.5-4v-5.5c0-.8284.6716-1.5 1.5-1.5s1.5.6716 1.5 1.5V18c0 1.6569-1.3431 3-3 3s-3-1.3431-3-3v-4",vectorEffect:"non-scaling-stroke"})});var E=n(99692);function O(e){let{attachments:t,onRemove:n,downloadable:i,optimizeImageUrl:a}=e;return 0===t.length?null:(0,r.jsx)(N.k,{gap:"2",p:"2",children:t.map(e=>{let t=e.name.slice(e.name.lastIndexOf(".")+1),o=e.type.startsWith("image/"),s=a?a(e.src,{width:168}):e.src,l=o?(0,r.jsx)(F,{children:(0,r.jsx)("img",{src:s,alt:e.name})}):(0,r.jsxs)(U,{direction:"column",align:"center",justify:"center",pt:"1",children:[(0,r.jsx)(D,{}),(0,r.jsx)(L.x,{as:"span",variant:"label-xs",children:"."+t})]});return(0,r.jsxs)(Z,{children:[(0,r.jsx)(R.u,{sideOffset:10,content:e.name,children:i?(0,r.jsx)(P,{target:"_blank",href:e.src,download:e.name,children:l}):l}),n&&(0,r.jsx)(W,{size:"1",color:"gray",variant:"solid",onClick:()=>n(e.id),children:(0,r.jsx)(E.A,{size:12})})]},e.id)})})}let Z=(0,i.Z)(N.k)`
  position: relative;
`,P=i.Z.a`
  cursor: pointer;
  text-decoration: none;
  color: inherit;
`,F=(0,i.Z)(N.k)`
  border-radius: var(--radius-3);
  box-shadow: var(--shadow-3);
  overflow: hidden;

  img {
    width: 56px;
    height: 56px;
    object-fit: cover;
  }
`,U=(0,i.Z)(N.k)`
  width: 56px;
  height: 56px;
  border-radius: var(--radius-3);
  background: var(--gray-a3);
  color: var(--gray-11);
`,W=(0,i.Z)(z.h)`
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
`;var B=n(62563),G=n(2350);let J="file-drop-over";function H(e){let t=e.dataTransfer;return!!t&&(t.files.length>0||Array.from(t.types).includes("Files"))}var _=n(1389),V=n(70822),Y=n(34220);let q=B.hj.create({name:"titlePlaceholder",addOptions:()=>({forceFocusDelay:null}),onCreate({editor:e}){e.commands.focus(K(e));let{forceFocusDelay:t}=this.options;null!==t&&setTimeout(()=>{e.isDestroyed||e.commands.focus(K(e))},t)},addProseMirrorPlugins:()=>[new G.Sy({key:new G.H$("sendToAppPlaceholder"),props:{decorations(e){let{doc:t}=e,n=[],r=!1,i=!1;return t.forEach((e,t,n)=>{0===n&&"heading"===e.type.name&&(r=!0),n>0&&e.childCount>0&&(i=!0)}),t.forEach((e,t,a)=>{var o,s,l;if(e.childCount>0)return;let d=(o=e,s=a,l={hasHeading:r,hasBodyContent:i},0===s&&"heading"===o.type.name?"Title":"paragraph"!==o.type.name||l.hasBodyContent?null:1!==s&&(0!==s||l.hasHeading)?null:"Write a description or @ to mention");d&&n.push(V.p.node(t,t+e.nodeSize,{class:"is-empty","data-placeholder":d}))}),V.EH.create(t,n)}}})]});function K(e){return"disabled"!==(0,Y.yt)(e)?"start":e.getText().trim().length>0?"end":"start"}var Q=n(47209),X=n(25755);let ee=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M17.5 5.2558V16.5c0 3.0376-2.4624 5.5-5.5 5.5s-5.5-2.4624-5.5-5.5V5.6667C6.5 3.6417 8.1416 2 10.1667 2c2.025 0 3.6666 1.6416 3.6666 3.6667v10.779c0 1.0126-.8208 1.8334-1.8333 1.8334s-1.8333-.8208-1.8333-1.8334V6.6512",vectorEffect:"non-scaling-stroke"})});var et=n(20305),en=n(50194),er=n(64410),ei=n(75818);let ea=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M7 17 17 7m0 0H7m10 0v10",vectorEffect:"non-scaling-stroke"})}),eo=(0,c.Pi)(function(e){let{onUpgrade:t,limitReached:n,feature:i}=e,[a,o]=(0,u.useState)(!1);return a?null:(0,r.jsxs)(es,{color:n?"amber":"blue",variant:"soft",size:"1",children:[n?(0,r.jsx)(er.JO,{children:(0,r.jsx)(ei.u,{size:16})}):null,(0,r.jsx)(er.xv,{size:"2",weight:"medium",children:(0,r.jsxs)(N.k,{gap:"2",direction:"column",align:"start",children:[e.text,(0,r.jsxs)(M.z,{size:"1",variant:"outline",onClick:()=>t(i),children:["Upgrade",(0,r.jsx)(ea,{size:14})]})]})}),n?null:(0,r.jsx)(el,{role:"button",tabIndex:0,onClick:()=>o(!0),children:(0,r.jsx)(E.A,{size:12})})]})}),es=(0,i.Z)(er.fC)`
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  width: 100%;
`,el=i.Z.div`
  position: absolute;
  right: -10px;
  top: -10px;
  display: flex;
  padding: var(--space-1);
  border-radius: 100%;
  background-color: var(--gray-1);
  border: 1px solid var(--gray-a6);
  box-shadow: var(--shadow-4);
  color: var(--gray-11);
  cursor: pointer;
  transition: color 0.2s ease-in-out;

  &:hover {
    color: var(--gray-12);
  }
`,ed=e=>e.numDemoUsesRemaining??e.store.numDemoUsesRemaining(e.feature);var ec=n(7656);let eu=(0,ec.T)({BR000:"0px",BR050:"2px",BR075:"4px",BR100:"8px",BR200:"10px",BR210:"12px",BR300:"16px",BR400:"20px",BR600:"40px",BR900:"70px",BRROUND:"99999px",BROVAL:"50%"});var ep=n(32748),eg=n(32760),em=n(76556),ex=n(6663);let eh=(0,c.Pi)(function(e){let[t,n]=u.useState(!1);if(t||e.store?.hasAccess(e.feature,e.teamId??"any"))return null;let i=ed(e),a=S.ZY[e.feature];return(0,r.jsxs)(ef,{children:[(0,r.jsx)(eb,{size:"bodyMedium",color:"black",weight:"medium",children:e.text(i,a)}),(0,r.jsx)(ev,{onClick:()=>e.onUpgrade(e.feature),size:"small",variant:"solid",appearance:"light",textType:"body",rounded:!1,children:"Upgrade"}),e.dismissable&&0===i?(0,r.jsx)(ew,{role:"button",tabIndex:0,onClick:()=>n(!0),children:(0,r.jsx)(E.A,{size:16})}):null]})}),ef=i.Z.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${eg.W.SP150};
  background-color: #f2ecfe;
  border-radius: ${eu.BR200};
  width: 100%;
`,ev=(0,i.Z)(em.z)`
  margin-left: auto;
  font-weight: ${ep.v.medium};
`,eb=(0,i.Z)(ex.x)`
  padding: 0px ${eg.W.SP200};
`,ew=i.Z.div`
  padding: 0px ${eg.W.SP200};
  cursor: pointer;
`;var ey=n(61525),eC=n(49255),ej=n(72321),eS=n(884);function ek(e,t,n){ej._z.info("Redirecting to upgrade flow",{teamId:e,feature:t});let r=new URL("s/upgrade",eS.v.DASH_URL);r.search=new URLSearchParams({[$.t1.CAMPAIGN]:t,...n}).toString(),window.open(r.toString(),"_blank")}var eI=n(49710),e$=n(84869),eA=n.n(e$);function eT(e){if(!e)return"Unknown User";let t=e.firstName?.trim(),n=e.lastName?.trim();if(t&&n)return`${t} ${n}`;if(t)return t;if(n)return n;let r=e.name?.trim();if(r)return r;let i=e.email?.trim();if(i){let e=i.split("@")[0];if(e)return e}return"Unknown User"}var eN=n(79976),eR=n(42494);let ez=new G.H$("jamMentionSuggestion"),eM=(0,i.Z)(eN.q)`
  padding: calc(var(--space-1) / 2);
`,eL=(0,i.Z)(L.x)`
  line-height: 20px;
  height: 20px;
`;var eD=n(75514);function eE(e){if(null==e)return 0;let t=new Date(e).getTime();return Number.isFinite(t)?t:0}let eO=(0,ec.T)({SHADOW1:"0px 8px 8px -4px rgba(64, 1, 17, 0.02), 0px 4px 4px -2px rgba(64, 1, 17, 0.02), 0px 2px 2px -1px rgba(42, 51, 69, 0.01), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.01), 0px 0.5px 0.5px -0.25px rgba(42, 51, 69, 0.01), 0px 0px 0px 1px rgba(64, 1, 17, 0.01)",SHADOW2:"0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(64, 1, 17, 0.0156863), 0px 4px 4px -2px rgba(42, 51, 69, 0.0156863), 0px 2px 2px -1px rgba(42, 51, 69, 0.0156863), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.0156863), 0px 0px 0px 1px rgba(64, 1, 17, 0.0156863)",SHADOW3:"0px 24px 24px -12px rgba(64, 1, 17, 0.0470588), 0px 12px 12px -6px rgba(64, 1, 17, 0.0235294), 0px 6px 6px -3px rgba(42, 51, 69, 0.0235294), 0px 3px 3px -1.5px rgba(42, 51, 69, 0.0235294), 0px 1.5px 1.5px -0.75px rgba(42, 51, 69, 0.0235294), 0px 0px 0px 1px rgba(64, 1, 17, 0.0235294)",SHADOW4:"0px 32px 32px -16px rgba(64, 1, 17, 0.0627451), 0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(42, 51, 69, 0.0313726), 0px 4px 4px -2px rgba(42, 51, 69, 0.0313726), 0px 2px 2px -1px rgba(42, 51, 69, 0.0313726), 0px 0px 0px 1px rgba(64, 1, 17, 0.0313726)",SHADOW5:"0px 24px 24px -12px rgba(64, 1, 17, 0.0627451), 0px 12px 12px -6px rgba(64, 1, 17, 0.0313726), 0px 6px 6px -3px rgba(42, 51, 70, 0.0313726), 0px 3px 3px -1.5px rgba(42, 51, 70, 0.0313726), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.0313726), 0px 0px 0px 1px rgba(64, 1, 17, 0.0313726)",SHADOW6:"0px 32px 32px -16px rgba(64, 1, 17, 0.0627451), 0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(42, 51, 69, 0.0313726), 0px 4px 4px -2px rgba(42, 51, 69, 0.0313726), 0px 2px 2px -1px rgba(42, 51, 69, 0.0313726), 0px 0px 0px 1px rgba(64, 1, 17, 0.0313726)",SHADOW7:"0px 24px 24px -12px rgba(64, 1, 17, 0.0470588), 0px 12px 12px -6px rgba(64, 1, 17, 0.0235294), 0px 6px 6px -3px rgba(42, 51, 69, 0.0235294), 0px 3px 3px -1.5px rgba(42, 51, 69, 0.0235294), 0px 1.5px 1.5px -0.75px rgba(42, 51, 69, 0.0235294), 0px 0px 0px 1px rgba(64, 1, 17, 0.0235294)",SHADOW8:"0px 16px 16px -8px rgba(64, 1, 17, 0.0313726), 0px 8px 8px -4px rgba(64, 1, 17, 0.0156863), 0px 4px 4px -2px rgba(42, 51, 69, 0.0156863), 0px 2px 2px -1px rgba(42, 51, 69, 0.0156863), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.0156863), 0px 0px 0px 1px rgba(64, 1, 17, 0.0156863)",SHADOW9:"0px 8px 8px -4px rgba(64, 1, 17, 0.02), 0px 4px 4px -2px rgba(64, 1, 17, 0.02), 0px 2px 2px -1px rgba(42, 51, 69, 0.01), 0px 1px 1px -0.5px rgba(42, 51, 69, 0.01), 0px 0.5px 0.5px -0.25px rgba(42, 51, 69, 0.01), 0px 0px 0px 1px rgba(64, 1, 17, 0.01)"}),eZ=i.Z.div`
  align-self: stretch;
  display: flex;
  align-items: center;
  margin-bottom: ${eg.W.SP600};
`,eP=i.Z.button`
  display: flex;
  height: 40px;
  justify-content: center;
  align-items: center;
  gap: ${eg.W.SP200};
  padding: ${eg.W.SP200} ${eg.W.SP300};
  border-radius: ${eu.BR100};
  background: ${eC.O.white};
  box-shadow: ${eO.SHADOW2}, 0px 0px 0px 1px rgba(0, 0, 0, 0.03);
`,eF=function(e){let{closeJam:t,resumedDraft:n}=e;return(0,r.jsx)(eZ,{children:(0,r.jsxs)(eP,{onClick:function(e){e.stopPropagation(),n?t({showToast:!0,storeDraft:!0}):t()},children:[(0,r.jsx)(E.A,{color:eC.O.charcoalGrey,size:16}),n&&(0,r.jsx)(L.x,{variant:"label-s",color:"primary",children:"Save for later"})]})})};function eU(e){return(0,r.jsxs)(eW,{className:e.className,children:[(0,r.jsx)(eB,{color:e.color}),(0,r.jsx)(eB,{color:e.color}),(0,r.jsx)(eB,{color:e.color})]})}let eW=i.Z.div`
  display: flex;
  align-items: center;
`,eB=i.Z.span`
  display: inline-block;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  margin-right: 2px;
  background: ${e=>eC.O[e.color]};
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
`;var eG=n(17029);let eJ=()=>(0,r.jsxs)(eH,{type:"button",children:[(0,r.jsx)(eV,{children:"Accept"})," ",(0,r.jsx)(e_,{children:"Tab"})]}),eH=i.Z.button`
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
`,e_=i.Z.kbd`
  display: flex;
  height: 16px;
  line-height: 16px;
  background: rgba(0, 0, 0, 0.04);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  font-size: 11px;
  padding: 0 4px;
`,eV=i.Z.span`
  line-height: 32px;
  font-size: 14px;
`,eY=Y.Vb.configure({renderAcceptButton:function(e){let t=document.createElement("div");return t.className="ghost-text-accept",t.addEventListener("mousedown",t=>{t.preventDefault(),e()}),(0,eG.createRoot)(t).render(u.createElement(eJ)),t},renderSpinner:function(){let e=document.createElement("div");return e.className="ghost-text-loader",(0,eG.createRoot)(e).render(u.createElement(eU,{color:"darkGrape"})),e}});var eq=n(94338);let eK=({highContrast:e=!0,...t})=>(0,r.jsx)(eq.r,{highContrast:e,...t});function eQ(e){return(0,r.jsxs)(N.k,{align:"center",gap:"2",mx:"1",children:[(0,r.jsx)(L.x,{variant:"label-s",children:"AI"}),(0,r.jsx)(R.u,{content:e.lockedReason,hidden:!e.locked,children:(0,r.jsx)(eK,{size:"1",checked:e.enabled,disabled:e.locked,onCheckedChange:e.onChange})})]})}var eX=n(37105);let e0=(0,i.Z)(eX.ck)`
  /* Default state styling */
  &.rt-DropdownMenuItem {
    font-weight: var(--font-weight-medium);
  }

  /* Unified hover state - works for any color, defaults to gray */
  &.rt-DropdownMenuItem:hover {
    ${e=>`background-color: var(--${e.color||"gray"}-a3);`}
  }
`,e1=(0,i.Z)(eX.fF)`
  /* SubTrigger font-weight override */
  &.rt-DropdownMenuSubTrigger {
    font-weight: var(--font-weight-medium);
  }

  /* Unified hover state - works for any color, defaults to gray */
  &.rt-DropdownMenuSubTrigger:hover {
    ${e=>`background-color: var(--${e.color||"gray"}-a3);`}
  }
`,e2=(0,i.Z)(eX.tu)`
  /* SubContent items font-weight override */
  .rt-DropdownMenuItem {
    font-weight: var(--font-weight-medium);
  }
`,e5=u.forwardRef((e,t)=>{let{color:n="gray",...i}=e;return(0,r.jsx)(eX.VY,{ref:t,variant:"soft",color:n,...i})});e5.displayName="DropdownMenuContent";let e6={Root:eX.fC,Trigger:eX.xz,Content:e5,Item:e0,Separator:eX.Z0,Label:eX.__,Sub:eX.Tr,SubTrigger:e1,SubContent:e2,RadioGroup:eX.Ee,RadioItem:eX.Rk},e3=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"m13 7-1.1155-2.231c-.3211-.6422-.4816-.9633-.7211-1.1978a2 2 0 0 0-.7473-.4619C10.0992 3 9.7402 3 9.0223 3H5.2c-1.1201 0-1.6802 0-2.108.218a2 2 0 0 0-.874.874C2 4.5198 2 5.08 2 6.2V7m0 0h15.2c1.6802 0 2.5202 0 3.162.327a3 3 0 0 1 1.311 1.311C22 9.2798 22 10.1198 22 11.8v4.4c0 1.6802 0 2.5202-.327 3.162a3 3 0 0 1-1.311 1.311C19.7202 21 18.8802 21 17.2 21H6.8c-1.6802 0-2.5202 0-3.162-.327a3 3 0 0 1-1.311-1.311C2 18.7202 2 17.8802 2 16.2z",vectorEffect:"non-scaling-stroke"})}),e7=(0,c.Pi)(e=>{let{foldersStore:t}=e,n=t.availableFolders,i=t.selectedFolder;return 0===n.length?null:(0,r.jsxs)(e6.Root,{children:[(0,r.jsx)(R.u,{content:"Select folder",children:(0,r.jsx)(e6.Trigger,{children:i?(0,r.jsxs)(e4,{size:"1",variant:"ghost",color:"gray",children:[(0,r.jsx)(N.k,{flexShrink:"0",children:(0,r.jsx)(e3,{size:16})}),(0,r.jsx)(L.x,{truncate:!0,variant:"label-s",children:i.name})]}):(0,r.jsx)(z.h,{size:"1",variant:"ghost",color:"gray",children:(0,r.jsx)(e3,{size:16})})})}),(0,r.jsxs)(e6.Content,{children:[(0,r.jsx)(e6.Item,{onSelect:()=>t.selectFolderById(),children:"No folder"}),n.map(e=>(0,r.jsx)(e6.Item,{onSelect:()=>t.selectFolderById(e.id),children:(0,r.jsxs)(N.k,{gap:"2",align:"center",children:[(0,r.jsx)(e3,{}),(0,r.jsx)(L.x,{children:e.name})]})},e.id))]})]})});e7.displayName="DraftFolderSelect";let e4=(0,i.Z)(M.z)`
  display: flex;
  flex: 0 1 auto;
  min-width: 0;
  white-space: nowrap;
  text-overflow: ellipsis;
`;var e9=n(72986),e8=n(3311);let te=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M9 17H7c-2.7614 0-5-2.2386-5-5s2.2386-5 5-5h2m6 10h2c2.7614 0 5-2.2386 5-5s-2.2386-5-5-5h-2m-8 5h10",vectorEffect:"non-scaling-stroke"})});var tt=n(22970),tn=n(28165);let tr=i.Z.div`
  ${function(e){return(0,tn.iv)`
    padding: ${e.padding};
    margin: ${e.margin};
    background: ${eC.O[e.background]};
    border-radius: ${e.borderRadius};
    border: ${e.borderColor?`1px solid ${eC.O[e.borderColor]}`:"none"};
  `}}
`;function ti(e,t){if(t)return Array.isArray(t)?t.map(t=>e[t]).join(" "):e[t]}function ta(e){let{align:t,alignSelf:n,justify:i,direction:a,gap:o,wrap:s,grow:l,shrink:d,basis:c,dir:u,inline:p,width:g,...m}=e,x={align:t,justify:i,direction:u??a,alignSelf:n,gap:o&&eg.W[o],wrap:s,grow:l,shrink:d,basis:c,inline:p,width:g,className:e.className??void 0};return(0,r.jsx)(to,{...x,...m,children:e.children})}let to=(0,i.Z)(function(e){let t={padding:ti(eg.W,e.padding),margin:ti(eg.W,e.margin),background:e.background??"transparent",borderRadius:ti(eu,e.borderRadius),borderColor:e.borderColor};return(0,r.jsx)(tr,{...t,className:e.className,children:e.children})})`
  display: ${e=>e.inline?"inline-flex":"flex"};
  ${function(e){return(0,tn.iv)`
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
`;function ts(e){let{fillStroke:t="#2A3632",...n}=e;return(0,r.jsxs)(tl,{...n,viewBox:"0 0 18 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,r.jsx)("path",{d:"M11.609 15.4909C11.018 15.25 10.4089 15 8.99986 15C7.59077 15 6.97713 15.25 6.39077 15.4909C6.22259 15.5591 6.04986 15.6273 5.86349 15.6909C5.38168 16.2682 5.15895 17.0636 5.27258 17.8364C5.33622 18.2773 5.72258 18.6091 6.17258 18.6091C6.21804 18.6091 6.26349 18.6045 6.31349 18.6C6.77258 18.5318 7.12258 18.3636 7.38622 18.1818C7.57713 18.6318 7.94077 19.1364 8.64531 19.4409C8.75895 19.4909 8.87713 19.5136 9.0044 19.5136C9.13168 19.5136 9.24986 19.4909 9.36349 19.4409C10.068 19.1409 10.4317 18.6318 10.6226 18.1818C10.8862 18.3636 11.2362 18.5273 11.6953 18.6C11.7408 18.6091 11.7862 18.6091 11.8362 18.6091C12.2862 18.6091 12.6726 18.2773 12.7362 17.8364C12.8453 17.0636 12.6271 16.2682 12.1453 15.6909C11.9499 15.6273 11.7817 15.5591 11.609 15.4909Z",fill:"#73E5BF"}),(0,r.jsx)("path",{d:"M13.5454 15.9091C12.6409 15.9091 12.1182 15.6954 11.6091 15.4909C11.0182 15.25 10.4091 15 8.99998 15C7.59089 15 6.97725 15.25 6.39089 15.4909C5.88634 15.6954 5.36361 15.9091 4.45452 15.9091C3.4227 15.9091 2.62725 15.6363 2.08634 15.0954C1.54543 14.5545 1.27271 13.7591 1.27271 12.7273C1.27271 10.0409 2.14543 6.97726 3.60907 4.54089C5.16816 1.94544 7.1318 0.454529 8.99998 0.454529C10.8682 0.454529 12.8318 1.94544 14.3909 4.54089C15.8545 6.9818 16.7273 10.0409 16.7273 12.7273C16.7273 13.7591 16.4545 14.5545 15.9136 15.0954C15.3727 15.6363 14.5772 15.9091 13.5454 15.9091Z",fill:"#FF4070"}),(0,r.jsx)("path",{d:"M6.95452 9.09089C6.72725 9.09089 6.27271 9.09089 6.27271 10.2273C6.27271 11.3636 6.72725 11.3636 6.95452 11.3636C7.1818 11.3636 7.63634 11.3636 7.63634 10.2273C7.63634 9.09089 7.1818 9.09089 6.95452 9.09089Z",fill:t}),(0,r.jsx)("path",{d:"M11.0454 9.09089C10.8182 9.09089 10.3636 9.09089 10.3636 10.2273C10.3636 11.3636 10.8182 11.3636 11.0454 11.3636C11.2727 11.3636 11.7273 11.3636 11.7273 10.2273C11.7273 9.09089 11.2727 9.09089 11.0454 9.09089Z",fill:t}),(0,r.jsx)("path",{d:"M8.99998 5.45453C8.77271 5.45453 8.31816 5.45453 8.31816 6.59089C8.31816 7.72726 8.77271 7.72726 8.99998 7.72726C9.22725 7.72726 9.6818 7.72726 9.6818 6.59089C9.6818 5.45453 9.22725 5.45453 8.99998 5.45453Z",fill:t}),(0,r.jsx)("path",{d:"M16.5228 8.32273C16.1091 6.9 15.5046 5.50909 14.7819 4.30455C14.0319 3.05455 13.1546 2.00909 12.241 1.27727C11.1773 0.431818 10.0864 0 9.00006 0C7.91369 0 6.82278 0.431818 5.76369 1.27727C4.85005 2.00909 3.97278 3.05455 3.22278 4.30455C2.50006 5.50909 1.89551 6.9 1.48187 8.32273C1.04551 9.80909 0.818237 11.3318 0.818237 12.7273C0.818237 13.8818 1.13642 14.7864 1.76824 15.4136C2.39551 16.0455 3.30006 16.3636 4.4546 16.3636C4.64551 16.3636 4.81824 16.3545 4.98187 16.3409C4.8046 16.8318 4.74551 17.3727 4.82278 17.9C4.91824 18.5636 5.50005 19.0636 6.17278 19.0636C6.24096 19.0636 6.31369 19.0591 6.38187 19.0455C6.69551 18.9955 6.97278 18.9091 7.2046 18.8045C7.5046 19.2682 7.93187 19.6273 8.46369 19.8545C8.63642 19.9273 8.81369 19.9636 9.00006 19.9636C9.18642 19.9636 9.36824 19.9273 9.53642 19.8545C10.0682 19.6273 10.4955 19.2682 10.7955 18.8045C11.0319 18.9091 11.3046 18.9955 11.6182 19.0455C11.6864 19.0545 11.7591 19.0591 11.8273 19.0591C12.5001 19.0591 13.0819 18.5591 13.1773 17.8955C13.2546 17.3682 13.1955 16.8273 13.0182 16.3364C13.1819 16.35 13.3546 16.3591 13.5455 16.3591C14.7001 16.3591 15.6046 16.0409 16.2319 15.4091C16.8637 14.7864 17.1819 13.8818 17.1819 12.7273C17.1819 11.3318 16.9546 9.80909 16.5228 8.32273ZM12.2773 17.7682C12.2455 17.9955 12.0501 18.1545 11.8273 18.1545C11.8046 18.1545 11.7819 18.1545 11.7591 18.15C10.7228 17.9909 10.3637 17.2727 10.3637 17.2727C10.3637 17.2727 10.3637 18.5136 9.17733 19.0227C9.11824 19.0455 9.05915 19.0591 9.00006 19.0591C8.94096 19.0591 8.87733 19.0455 8.82278 19.0227C7.63642 18.5136 7.63642 17.2727 7.63642 17.2727C7.63642 17.2727 7.27733 17.9909 6.24096 18.15C6.21824 18.1545 6.19551 18.1545 6.17278 18.1545C5.95005 18.1545 5.7546 17.9955 5.72278 17.7682C5.63187 17.1227 5.81824 16.5091 6.13642 16.0727C6.28642 16.0182 6.42733 15.9636 6.55915 15.9091C7.13187 15.6727 7.67733 15.4545 9.00006 15.4545C10.3228 15.4545 10.8637 15.6773 11.441 15.9091C11.5773 15.9636 11.7137 16.0227 11.8637 16.0727C12.1819 16.5091 12.3728 17.1227 12.2773 17.7682ZM13.5455 15.4545C11.7273 15.4545 11.7273 14.5455 9.00006 14.5455C6.27278 14.5455 6.27278 15.4545 4.4546 15.4545C2.63642 15.4545 1.72733 14.5455 1.72733 12.7273C1.72733 7.27273 5.36369 0.909091 9.00006 0.909091C12.6364 0.909091 16.2728 7.27273 16.2728 12.7273C16.2728 14.5455 15.3637 15.4545 13.5455 15.4545Z",fill:t})]})}let tl=i.Z.svg`
  vertical-align: middle;
`;function td(e){return(0,r.jsx)(tc,{autoMargin:e.autoMargin??!0,className:e.className,children:(0,r.jsx)(ts,{height:24,width:24})})}let tc=i.Z.div`
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
`;var tu=n(6757);let tp=i.Z.button`
  display: grid;
  align-items: center;
  grid-template-columns: 24px 20px;
  border-radius: ${eg.W.SP200};
  padding: ${eg.W.SP200} ${eg.W.SP250};
  gap: ${eg.W.SP200};
  background: ${eC.O.white};
  border: 1px solid ${eC.O.mediumGrey};
  box-shadow: ${eO.SHADOW1};
`,tg=i.Z.div`
  background: ${eC.O.black};
  display: flex;
  flex-direction: column;
  max-width: 260px;
  width: 100%;
  overflow: hidden;
  padding: ${eg.W.SP100};
`,tm=i.Z.button`
  width: 100%;
  background: transparent;
  padding: ${eg.W.SP100} ${eg.W.SP400};
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
    background: ${eC.O.nearBlack};
  }
`,tx=i.Z.div`
  height: 1px;
  background: ${eC.O.nearBlack};
  margin: ${eg.W.SP200} ${eg.W.SP400};
`;var th=n(40807),tf=n(59802),tv=n(17620),tb=n.n(tv),tw=n(92622),ty=n(89825);let tC=(0,c.Pi)(function(e){let{integration:t,unlocked:n=!0}=e,i=t.userConfigured&&t.teamConfigured,a=!i&&!t.allowConnecting,o=(0,r.jsxs)(tk,{disabled:!n||!t.allowConnecting&&!i,onClick:e.onClick,children:[e.icon??null,(0,r.jsx)(tj,{unlocked:n,integration:t,isConfigured:i}),e.active&&(0,r.jsx)(tw.J,{color:n?eC.O.white:eC.O.darkGrey}),a&&(0,r.jsx)(ei.u,{color:eC.O.mango})]},t.integrationName);return a?(0,r.jsx)(ty.u,{title:(0,e9.w5)(t.displayName),children:o}):o});function tj(e){let t=e.integration.integrationName,n=(0,e9._g)(t),i=e.integration.displayName,a="darkGrey";return(e.isConfigured&&(a=e.unlocked?"white":"darkGrey"),e.isConfigured)?(0,r.jsx)(tS,{color:a,children:i+" "+n}):(0,r.jsxs)(ta,{gap:"SP100",children:[(0,r.jsx)(ex.x,{as:"span",color:a,weight:"regular",size:"bodyMedium",children:"Connect"}),(0,r.jsx)(tS,{color:a,children:i})]})}let tS=(0,i.Z)(e=>(0,r.jsx)(ex.x,{as:"span",weight:"regular",size:"bodyMedium",...tb()(e,"unlocked")}))``,tk=(0,i.Z)(e=>(0,r.jsx)(tm,{...tb()(e,"$isConfigured")}))`
  grid-template-columns: 20px minmax(0, 1fr) 20px;

  svg:first-of-type {
    display: block;
    width: 20px;
  }

  &:disabled svg:first-of-type {
    filter: grayscale(1) sepia(0.8) saturate(0) brightness(0.7);
  }
`,tI={userConfigured:!0,teamConfigured:!0,allowConnecting:!0,integrationName:"link",displayName:"Link to share"},t$=(0,c.Pi)(e=>{let{excludeInternalIntegrations:t,teamEntitlements:n,integrations:i,onSelectIntegration:a,onClearSelectedIntegration:o,onConnectMoreApps:s,excludeEmailIntegration:l,excludeLinkOption:d}=e,c={teamId:e.teamId,integrations:i,onSelectIntegration:a,onClearSelectedIntegration:o,onConnectMoreApps:s,excludeInternalIntegrations:t,excludeEmailIntegration:l,excludeLinkOption:d,hasEntitlement:n.has};return(0,r.jsx)(tA,{...c})}),tA=(0,c.Pi)(e=>{let t=e.integrations.userConfiguredIntegrationsExcludingEmail(e.teamId)>=2,n=e.integrations.selectedIntegrationPerTeam.get(e.teamId);return(0,r.jsxs)(u.Fragment,{children:[e.excludeLinkOption?null:(0,r.jsx)(tC,{active:!n,unlocked:!0,integration:tI,icon:(0,r.jsx)(te,{color:"white",size:20}),onClick:e.onClearSelectedIntegration}),(0,r.jsx)(()=>{let i=e.integrations.getBy(e.teamId,{filterBy:"dataPushNotIssueTracker",sortBy:"standard"}).filter(t=>!e.excludeInternalIntegrations||!t.internal).filter(t=>!e.excludeEmailIntegration||"email"!==t.integrationName).filter(e=>"intercom"!==e.integrationName).filter(e=>!t||e.userConfigured);return(0,r.jsx)(r.Fragment,{children:i.map(t=>(0,r.jsx)(tC,{active:t.integrationName===n?.integrationName,integration:t,icon:(0,tt.fK)(t.integrationName),onClick:()=>e.onSelectIntegration(t)},t.id))})},{}),(0,r.jsx)(()=>e.integrations.getBy(e.teamId,{filterBy:"dataPushIssueTracker",sortBy:"standard"}).filter(t=>!e.excludeInternalIntegrations||!t.internal).filter(t=>!e.excludeEmailIntegration||"email"!==t.integrationName).filter(e=>"intercom"!==e.integrationName).filter(e=>!t||e.userConfigured).map(t=>(0,r.jsx)(tC,{active:t.integrationName===n?.integrationName,integration:t,icon:(0,tt.fK)(t.integrationName),onClick:()=>e.onSelectIntegration(t)},t.id)),{}),t?(0,r.jsx)(tT,{onClick:e.onConnectMoreApps,icon:(0,r.jsx)(tf.v,{}),appearance:"dark",textType:"body",children:"Connect more apps"}):null]})}),tT=(0,i.Z)(em.z)`
  justify-content: flex-end;
  padding: 8px 16px;
  border-radius: 0;
  border: none;
  line-height: 1;
  color: ${eC.O.darkGrey};

  svg {
    color: ${eC.O.darkGrey} !important;
    margin-right: 12px;
    width: 20px;
  }

  span {
    font-size: ${th.C.bodyMedium};
    font-weight: ${ep.v.regular};
  }

  &:hover,
  &:focus {
    background: ${eC.O.nearBlack};
    border-color: ${eC.O.charcoalGrey};
    span,
    svg {
      color: ${eC.O.darkGrey} !important;
    }
  }
`,tN=e=>(0,r.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:e.size??20,height:e.size??20,fill:"none",viewBox:"0 0 24 24",strokeWidth:"1.5",...e,children:(0,r.jsx)("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",d:"M7.101 10H7V8c0-2.7614 2.2386-5 5-5s5 2.2386 5 5v2h-.101M12 14v2m7-1c0 3.866-3.134 7-7 7s-7-3.134-7-7 3.134-7 7-7 7 3.134 7 7",vectorEffect:"non-scaling-stroke"})});var tR=n(14269),tz=n(97784);function tM(e){let t=e.src??void 0;t?.includes("avatars.jam.dev")&&(t=void 0);let n=e.firstLetter.toUpperCase(),i=e.borderRadius??"6px",a=e.size??24,o=tO[n]??"lime",s=tZ(o),l=tP(o);return(0,r.jsxs)(tL,{size:a,children:[(0,r.jsx)(tD,{src:t,alt:n,radius:i}),(0,r.jsx)(tE,{radius:i,size:a,style:{backgroundColor:s,color:l},children:n})]})}let tL=(0,i.Z)(tR.fC)`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  overflow: hidden;
  user-select: none;
  width: ${e=>e.size}px;
  height: ${e=>e.size}px;
  flex-shrink: 0;
`,tD=(0,i.Z)(tR.Ee)`
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: ${e=>e.radius};
`,tE=(0,i.Z)(tR.NY)`
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
`,tO={A:"blue",B:"amber",C:"lime",D:"amber",E:"crimson",F:"blue",G:"cyan",H:"blue",I:"amber",J:"lime",K:"amber",L:"crimson",M:"blue",N:"cyan",O:"blue",P:"amber",Q:"lime",R:"amber",S:"crimson",T:"blue",U:"cyan",V:"blue",W:"amber",X:"lime",Y:"amber",Z:"crimson"},tZ=e=>{switch(e){case"blue":return tz.iNS.blue3;case"amber":return tz.DzF.amber3;case"lime":return tz.LRo.lime3;case"crimson":return tz.WlT.crimson3;case"cyan":return tz.sl2.cyan3}},tP=e=>{switch(e){case"blue":return tz.iNS.blue11;case"amber":return tz.DzF.amber11;case"lime":return tz.LRo.lime11;case"crimson":return tz.WlT.crimson11;case"cyan":return tz.sl2.cyan11}};var tF=n(55607);function tU(e){let t=t=>{e.onSelectTeam(t),e.onClose()},{restrictedTeamIds:n}=e,i=e.normalTeams??[],a=n?i.filter(e=>!n.has(e.id)):i,o=n?i.filter(e=>n.has(e.id)):[];return(0,r.jsxs)(tg,{children:[(0,r.jsx)(tG,{children:(0,r.jsx)(ex.x,{color:"darkGrey",as:"span",size:"bodyMedium",weight:"medium",children:"Save to"})}),(0,r.jsx)(tx,{}),a.length>0?(0,r.jsx)(tH,{children:a.map(n=>(0,r.jsx)(tW,{onClick:t,selectedTeamId:e.selectedTeam?.id??null,team:n,avatar:n.logo},n.id))}):null,o.length>0?(0,r.jsxs)(u.Fragment,{children:[o.map(e=>(0,r.jsx)(tB,{team:e,avatar:e.logo},e.id)),e.restrictedFooter]}):null]})}let tW=e=>(0,r.jsxs)(tm,{onClick:()=>e.onClick(e.team.id),children:[(0,r.jsx)(tM,{firstLetter:e.team.name.charAt(0),src:e.avatar}),(0,r.jsx)(ex.x,{color:"white",truncate:!0,as:"span",weight:"medium",size:"bodyMedium",children:e.team.name}),e.selectedTeamId===e.team.id&&(0,r.jsx)(tw.J,{color:eC.O.white})]},e.team.id),tB=e=>(0,r.jsxs)(tJ,{as:"div",children:[(0,r.jsx)(tM,{firstLetter:e.team.name.charAt(0),src:e.avatar}),(0,r.jsx)(ex.x,{color:"darkGrey",truncate:!0,as:"span",weight:"medium",size:"bodyMedium",children:e.team.name}),(0,r.jsx)(tN,{size:16,color:eC.O.darkGrey})]}),tG=i.Z.div`
  height: 32px;
  align-items: center;
  display: flex;
  padding: 8px 16px;
`,tJ=(0,i.Z)(tm)`
  cursor: default;

  &:hover {
    background: transparent;
  }
`,tH=i.Z.div`
  display: flex;
  flex-direction: column;
  max-height: 320px;
  flex-direction: column;
  overflow-y: auto;

  ${tF.zl};
`,t_=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)(null),[i,a]=(0,u.useState)(!1),o=()=>{a(!1)},s=e.restrictedTeamIds?.has(e.selectedTeam.id)??!1;return(0,r.jsxs)("div",{children:[(0,r.jsx)("div",{ref:n,children:(0,r.jsxs)(tp,{onClick:()=>a(!0),children:[(0,r.jsx)(tM,{firstLetter:e.selectedTeam.name.charAt(0),src:e.selectedTeam.logo??void 0}),s?(0,r.jsx)(tN,{color:eC.O.charcoalGrey,size:16}):(0,r.jsx)(e8._,{color:eC.O.charcoalGrey})]})}),(0,r.jsx)(tu.J,{isOpen:i,anchorEl:t,onClose:o,disableAutoFocus:!0,borderRadius:12,anchorOrigin:{vertical:"bottom",horizontal:"right"},transformOrigin:{vertical:-4,horizontal:"right"},children:(0,r.jsx)(tU,{onClose:o,selectedTeam:e.selectedTeam,onSelectTeam:t=>{o(),e.onSelectTeam(t)},normalTeams:e.normalTeams,userAvatar:e.userAvatar,restrictedTeamIds:e.restrictedTeamIds,restrictedFooter:e.restrictedFooter})})]})}),tV=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)(null),[i,a]=(0,u.useState)(!1),{onOpen:o,waitingForAuth:s,...l}=e,{selectedIntegration:d}=e.integrations;(0,u.useEffect)(()=>{if(e.autoSelectNextActiveIntegration&&d&&!d?.userConfigured){let t=e.integrations.sortedAvailableIntegrations(e.team.id).find(e=>e.userConfigured&&e.teamConfigured);e.integrations.selectIntegration(t)}},[e.team.id,e.autoSelectNextActiveIntegration,e.integrations,d]);let c=()=>{e.onClose?.(),a(!1)};return(0,r.jsxs)(r.Fragment,{children:[e.headless?null:(0,r.jsxs)(tK,{children:[(0,r.jsx)(t0,{size:"bodyMedium",weight:"medium",color:"newGrey",children:"Create a"}),(0,r.jsxs)(tQ,{children:[(0,r.jsx)(t1,{ref:n,children:(0,r.jsx)(tq,{integrations:e.integrations,onOpen:()=>{a(!0),o?.()}})}),(e.normalTeams??[]).length>0&&(0,r.jsx)(t_,{selectedTeam:e.team,normalTeams:e.normalTeams,onSelectTeam:e.onSelectTeam,userAvatar:e.userAvatar,restrictedTeamIds:e.restrictedTeamIds,restrictedFooter:e.restrictedFooter})]})]}),(0,r.jsx)(tu.J,{isOpen:e.headless?.open??i,anchorEl:e.headless?.anchor??t,onClose:c,disableAutoFocus:!0,container:e.headless?.anchor??t,borderRadius:12,anchorOrigin:{vertical:"bottom",horizontal:"left"},transformOrigin:{vertical:-4,horizontal:0},children:(0,r.jsx)(tg,{children:(0,r.jsx)(tY,{...l,excludeEmailIntegration:!!e.headless,excludeLinkOption:!!e.headless,onSelectIntegration:e=>{c(),l.onSelectIntegration(e)},onClearSelectedIntegration:()=>{c(),l.onClearSelectedIntegration()},isLoading:e.isLoading&&!s})})})]})}),tY=(0,c.Pi)(e=>{let{isLoading:t,...n}=e;return t?(0,r.jsx)("div",{children:(0,r.jsx)(td,{})}):(0,r.jsx)(t$,{...n})}),tq=e=>{let t=e.integrations.selectedIntegration;return(0,r.jsxs)(tX,{onClick:e.onOpen,children:[void 0===t?(0,r.jsx)(te,{}):tt.Y6(t.integrationName),(0,r.jsx)(ex.x,{as:"span",truncate:!0,size:"bodyMedium",weight:"regular",children:(()=>{if(!t)return"Link to share";let e=(0,e9._g)(t.integrationName??"");return`${t.displayName} ${e}`})()}),(0,r.jsx)(ta,{grow:1,justify:"end",children:(0,r.jsx)(e8._,{color:eC.O.charcoalGrey})})]})},tK=i.Z.div`
  display: flex;
  align-items: center;
  gap: ${eg.W.SP200};
  min-width: 0;

  ${ey.w.tablet} {
    margin-bottom: 8px;
  }
`,tQ=i.Z.div`
  display: grid;
  grid-template-columns: 1fr auto;
  gap: ${eg.W.SP200};
  min-width: 0;
  flex-grow: 1;

  /* if user has only one team, let select button take full width */
  &:has(> :only-child) {
    grid-template-columns: 1fr;
  }
`,tX=i.Z.button`
  display: flex;
  align-items: center;
  border-radius: ${eg.W.SP200};
  padding: ${eg.W.SP200} ${eg.W.SP300};
  gap: ${eg.W.SP200};
  width: 100%;
  background: ${eC.O.white};
  border: 1px solid ${eC.O.mediumGrey};
  box-shadow: ${eO.SHADOW1};

  svg {
    flex: none;
  }

  svg:first-of-type {
    width: 20px;
    height: 20px;
  }
`,t0=(0,i.Z)(ex.x)`
  white-space: nowrap;
`,t1=i.Z.div`
  display: flex;
  flex: 1;
  min-width: 0;
`;var t2=n(44496);function t5(e){let t=(0,r.jsx)(t7,{children:(0,r.jsxs)(ta,{dir:"column",gap:"SP250",children:[(0,r.jsxs)(ex.x,{weight:"medium",size:"bodySmall",color:"white",children:["Now that your trial for workspace"," ",(0,r.jsx)("strong",{children:e.workspaceName})," has ended, new Jams you create will be visible to anyone with the link"]}),(0,r.jsxs)(ta,{justify:"space-between",children:[(0,r.jsx)(t3,{variant:"primary",onClick:e.onUpgradePlansClick,children:"Upgrade plans"}),(0,r.jsx)(t3,{variant:"secondary",onClick:e.onClose,children:"Dismiss"})]})]})});return(0,r.jsx)(ty.u,{open:e.open,placement:"bottom-start",title:t,disablePortal:!0,interactive:!0,children:e.children})}let t6=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)(!1),i=(0,g.fe)(),a=(0,g.$7)(),o=(0,g.MU)(),s=(0,t2.J)(o),l=i.filterByVariant("BusinessTrialEndedDashboard",a.selectedTeamId),d=l.length>0&&"teamId"in l[0]?l[0].teamId:"",c=a.teams?.find(e=>e.id===d)?.name??"unknown",p=(0,u.useRef)(new Set),m=(0,u.useRef)(new Set),x=(0,u.useCallback)(()=>{n(l.length>0),!(l.length>0)||l[0].deactivatedAt||p.current.has(l[0].id)||(s.viewInAppNotification({id:l[0].id}),p.current.add(l[0].id))},[s,JSON.stringify(l)]),h=(0,u.useCallback)(()=>{t&&(n(l.length>0),!(l.length>0)||l[0].deactivatedAt||m.current.has(l[0].id)||(s.deactivateInAppNotification({id:l[0].id}),m.current.add(l[0].id)))},[s,JSON.stringify(l)]);(0,u.useEffect)(()=>{x()},[x]);let f=(0,u.useCallback)(()=>{l.length>0&&(ek(d,S.AN.Unknown,{[$.t1.SOURCE]:"extension:iframe",[$.t1.CONTENT]:"business-trial-end"}),h())},[JSON.stringify(l)]);return(0,r.jsx)(t5,{workspaceName:c,open:t,onClose:h,onUpgradePlansClick:f,children:e.children})}),t3=i.Z.a`
  font-weight: ${ep.v.medium};
  font-size: ${th.C.bodySmall};

  &:hover {
    text-decoration: none;
  }

  ${e=>"primary"===e.variant?(0,tn.iv)`
        color: ${eC.O.blueberry};
        &:hover {
          color: ${eC.O.lightBlueberry};
        }
      `:(0,tn.iv)`
        color: ${eC.O.darkGrey};
        &:hover {
          color: ${eC.O.mediumGrey};
        }
      `}
`,t7=i.Z.div`
  max-width: 326px;
  text-wrap: wrap;
  padding: 5px 0;
`,t4=e=>{let t=`${eS.v.DASH_URL}/s/${e.teamId}/settings/members`;return(0,r.jsxs)(t9,{children:[(0,r.jsx)(ex.x,{color:"white",as:"span",weight:"medium",size:"bodyMedium",children:"Request upgrade"}),(0,r.jsx)(ex.x,{color:"darkGrey",as:"span",size:"bodySmall",children:"Your account needs to be upgraded to creator by an admin."}),(0,r.jsxs)(t8,{href:t,target:"_blank",rel:"noopener noreferrer",children:["View admins",(0,r.jsx)(ea,{size:16})]})]})},t9=i.Z.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 16px 12px;
`,t8=i.Z.a`
  margin-top: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: ${eC.O.leaf};
  color: ${eC.O.black};
  font-weight: 600;
  font-size: 14px;
  border-radius: 8px;
  padding: 8px 12px;
  text-decoration: none;

  /* This renders as a button, so override the iframe's global Bootstrap-derived
     anchor styling (a:hover { text-decoration: underline; color: blue }). */
  &:hover {
    color: ${eC.O.black};
    text-decoration: none;
    filter: brightness(0.96);
  }
`,ne=(0,c.Pi)(e=>{let{user:t}=(0,g.dR)(),{integrationsStore:n,authStore:i}=e,o=e.authStore.selectedTeamId,s=t?.teams.find(e=>e.id===o),d=(0,u.useRef)(!1);if((0,u.useEffect)(()=>{!n.availableIntegrationsLoading&&d.current&&((0,l.Y)().finalize("integrations_render_list","success"),d.current=!1)},[n.availableIntegrationsLoading]),(0,u.useEffect)(()=>{if(s?.roleType!==eI.GD.ViewerRestricted)return;let e=(t?.teams??[]).find(e=>e.roleType!==eI.GD.ViewerRestricted);e&&(i.setSelectedTeamId(e.id),n.setTeamId(e.id),n.setSelectedIntegration(e.id,void 0))},[s,t,i,n]),!s)return null;let c=(t?.teams??[]).filter(e=>e.roleType===eI.GD.ViewerRestricted),p=new Set(c.map(e=>e.id)),m=p.has(s.id)?s.id:c[0]?.id;async function x(e){i.setSelectedTeamId(e),n.setTeamId(e),n.setSelectedIntegration(e,void 0);let t=n.syncedDataStore?.getSelectedIntegration(e);t&&(await n.onIntegrationChange(t),n.syncContextDown())}return(0,r.jsx)(nt,{children:(0,r.jsx)(t6,{children:(0,r.jsx)(tV,{onOpen:()=>{let e=(0,l.Y)();n.availableIntegrationsLoading?(e.create("integrations_render_list",{createTimeout:a.eq("1s"),traceTimeout:a.eq("10s")}),d.current=!0):(0,l.Y)().create("integrations_render_list",{mode:"insert-finalized",state:{type:"finalized",variant:"success",createdAt:Date.now(),finalizedAt:Date.now()}})},userAvatar:i.me.data?.avatarSrc,autoSelectNextActiveIntegration:!0,normalTeams:i.normalTeams,restrictedTeamIds:p,restrictedFooter:m?(0,r.jsx)(t4,{teamId:m}):void 0,onSelectTeam:x,excludeInternalIntegrations:!1,integrations:n,teamId:s.id,team:s,teamEntitlements:e.myFeaturesStore,waitingForAuth:e.waitingForAuth,isLoading:n.availableIntegrationsLoading,onSelectIntegration:async t=>{t.userConfigured&&t.teamConfigured||e.setWaitingForAuth(t.integrationName),await n.onIntegrationChange(t.integrationName),n.syncContextDown(),n.syncSelectedTeamIntegrationUp()},onClearSelectedIntegration:()=>{n.clearSelectedIntegration(),n.syncSelectedTeamIntegrationUp()},onConnectMoreApps:()=>{window.open(`${eS.v.DASH_URL}/s/${s.id}/settings/connected-apps?${$.I4.CONNECT_MORE_APPS}=true`,"_blank")}})})})}),nt=i.Z.section`
  padding: 24px;
  border-top-right-radius: 16px;
  align-items: baseline;
  min-height: 68px;
  gap: 24px;
  overflow: visible;
`,nn={description:null,dismissed:!1,generationId:null,sessionId:null,status:"idle",title:null};async function nr(e,t,n){let r=(0,A.Z)(),i=await e.send({eventName:"GetAiSummary",dest:{component:s.wA.Main,location:void 0},data:{aiSessionId:n,localGenerationId:r,tabId:t.tabId,teamId:t.teamId,trigger:"mount"},timeout:a.eq("30s")});return i.ok?{description:i.value.description,dismissed:!1,generationId:i.value.generationId,sessionId:n,status:"ready",title:i.value.title}:{description:null,dismissed:!1,generationId:null,sessionId:n,status:"error",title:null}}function ni(e){return`${e.teamId}:${e.tabId}:${e.draftStartedAt??"none"}`}function na(e){return{description:e.description,dismissed:e.dismissed,generationId:e.generationId,sessionId:e.sessionId,status:e.status,title:e.title}}function no(e,t,n){let r=function(e){var t;let{state:n,hasTitle:r,ghostVisible:i,hasAcceptedContent:a}=e;if("error"===n.status)return i?{kind:"clear"}:{kind:"none"};if(n.dismissed||"idle"===n.status||a)return{kind:"none"};if("loading"===n.status)return{kind:"loading"};let o=(t=n,r&&t.title?`### ${t.title}

${t.description??""}`:t.description??null);return o?{kind:"suggest",text:o}:{kind:"none"}}({state:t,hasTitle:n,ghostVisible:"disabled"!==(0,Y.yt)(e),hasAcceptedContent:null!==ns(e)});switch(r.kind){case"clear":e.commands.clearSuggestion();break;case"loading":e.commands.setSuggestion(n?"### Add a title or wait for AI\n\nWrite a description or @ to mention":"Write a description or wait for AI",{showSpinner:!0});break;case"suggest":e.commands.setSuggestion(r.text,{showSpinner:!1})}}function ns(e){return"disabled"!==(0,Y.yt)(e)||0===e.getText().trim().length?null:e.getJSON()}function nl(e,t){return!e||e.type!==eI.Wz.None&&(e.type!==eI.Wz.Restricted||e.value.includes(t))}let nd=(0,c.Pi)(e=>{let{integrationsStore:t,inAppNotificationsStore:n,foldersStore:i,newThreadStore:o,authStore:l,globallySyncedStore:d}=e,{capture:c,teamFeatureUsage:p}=d,x=(0,u.useRef)(null),h=(0,u.useRef)(null),b=(0,g.MU)(),w=(0,g.z3)(),y=(0,m.i)();async function C(e){let n=t.getFileTypes(),{accepted:r,rejectedSizeCount:i,rejectedTypeCount:s,rejectedOverflowCount:l}=function(e,t){let{isTypeAllowed:n}=t,r=n?e.filter(e=>n(e)):e,i=e.length-r.length,a=r.filter(e=>e.size<=5e6),o=r.length-a.length,s=Math.max(0,t.maxFiles-t.currentCount),l=a.slice(0,s),d=a.length-l.length;return{accepted:l,rejectedSizeCount:o,rejectedTypeCount:i,rejectedOverflowCount:d}}(e,{currentCount:o.attachments.length,maxFiles:5,isTypeAllowed:e=>{var t;return!!(t=e.name)&&I.test(t)&&nl(n,e.type)}});l>0&&y({title:"You can attach up to 5 files",ttl:a.eq("3s"),dismissable:!0}),s>0&&y({title:`${s} unsupported ${eA()("file",s)}`,ttl:a.eq("3s"),dismissable:!0}),i>0&&y({title:`${i} ${eA()("file",i)} over the 5 MB limit`,ttl:a.eq("3s"),dismissable:!0}),0!==r.length&&o.addAttachments(await Promise.all(r.map(T)))}let j=(0,u.useRef)(C);j.current=C;let L=(0,u.useMemo)(()=>{var e;return e=e=>j.current(e),B.hj.create({name:"fileDrop",addProseMirrorPlugins(){let t=null,n=()=>{t&&(clearTimeout(t),t=null)},r=(e,t)=>{e.dom.classList.toggle("file-drop-active",t),t?e.dom.dataset.fileDropPlaceholder="Drop your files here":(delete e.dom.dataset.fileDropPlaceholder,e.dom.classList.remove(J))},i=(e,t)=>{let n=t.target;r(e,!0),e.dom.classList.toggle(J,n instanceof Node&&e.dom.contains(n))},a=e=>{n(),r(e,!1)},o=e=>{n(),t=setTimeout(()=>r(e,!1),100)};return[new G.Sy({props:{handleDOMEvents:{dragover:(e,t)=>!!H(t)&&(t.preventDefault(),!0),dragend:e=>(a(e),!1)},handleDrop:(t,n)=>{a(t);let r=Array.from(n.dataTransfer?.files??[]);return 0!==r.length&&(n.preventDefault(),e(r),!0)},handlePaste:(t,n)=>{let r=Array.from(n.clipboardData?.files??[]);return 0!==r.length&&(n.preventDefault(),e(r),!0)}},view(e){let t=e.dom.ownerDocument,r=t.defaultView,s=()=>a(e),l=t=>{H(t)&&(n(),i(e,t))},d=n=>{if(!H(n))return;let r=n.relatedTarget;!(r instanceof Node&&t.documentElement.contains(r))&&o(e)};return t.addEventListener("dragenter",l,!0),t.addEventListener("dragover",l,!0),t.addEventListener("dragleave",d,!0),t.addEventListener("drop",s,!0),t.addEventListener("dragend",s,!0),r?.addEventListener("blur",s),{destroy(){a(e),t.removeEventListener("dragenter",l,!0),t.removeEventListener("dragover",l,!0),t.removeEventListener("dragleave",d,!0),t.removeEventListener("drop",s,!0),t.removeEventListener("dragend",s,!0),r?.removeEventListener("blur",s)}}}})]}})},[]),D=l.selectedTeamId,E=l.me?.data?.id,Z=!t.syncedDataStore.loaded||!t.selectedIntegration||t.displayFields.has("title"),{mentionSuggestion:P}=function(e){let t=(0,g.$7)(),n=t.data?.id,i=t.data?.teams.find(t=>t.id===e)?.members,a=i?(0,eD.vM)(i):void 0,{mentionSuggestion:o}=function(e){let{members:t,resolveMember:n}=e,i=(0,u.useRef)(t);i.current=t;let a=(0,u.useRef)(n);return a.current=n,{mentionSuggestion:(0,u.useMemo)(()=>{var e;return e={membersRef:i,resolverRef:a},{buildExtension:t=>eR.Z.configure({hasResolver:()=>null!=e.resolverRef.current,resolveMember:t=>e.resolverRef.current?.(t)??null,suggestion:{char:"@",...t,allow:({state:e,range:t})=>"heading"!==e.doc.resolve(t.from).parent.type.name,command:({editor:e,range:t,props:n})=>(function({editor:e,range:t,member:n}){e.chain().focus().insertContentAt(t,[{type:"mention",attrs:{targetType:"user",targetId:n.id,label:n.name}},{type:"text",text:" "}]).run(),window.getSelection()?.collapseToEnd()})({editor:e,range:t,member:n})}}),getItemKey:e=>e.id,getSelectedValue:e=>e,id:"jamMentionSuggestion",items:({query:t})=>(function(e,t){let n=t.toLowerCase();return(n?e.filter(e=>e.displayName.toLowerCase().includes(n)||e.name.toLowerCase().includes(n)||(e.email?.toLowerCase().includes(n)??!1)):e).slice(0,10)})(e.membersRef.current,t),pluginKey:ez,renderItem:({item:e})=>(0,r.jsxs)(u.Fragment,{children:[(0,r.jsx)(eM,{src:e.avatarSrc??void 0,fallback:e.displayName.charAt(0),size:"1",radius:"full"}),(0,r.jsx)(eL,{as:"span",truncate:!0,children:e.displayName})]})}},[])}}({members:(0,u.useMemo)(()=>{var e;return(e=function(e,t){if(!e)return e;let n=null==t?[...e]:e.filter(e=>e.id!==t);return n.sort((e,t)=>{let n=eE(e.lastActiveAt),r=eE(t.lastActiveAt);return n!==r?r-n:eT(e).localeCompare(eT(t))}),n}(a,n))?e.map(e=>({id:e.id,displayName:eT(e),name:eT(e),email:e.email,avatarSrc:e.avatarSrc})):[]},[a,n]),resolveMember:(0,u.useMemo)(()=>(function(e){if(e)return t=>{let n=e.find(e=>e.id===t);return n?{name:eT(n),email:n.email,avatarSrc:n.avatarSrc}:null}})(a),[a])});return{mentionSuggestion:o}}(D),{emojiSuggestion:F}=(0,_.I)(),U=(0,u.useMemo)(()=>{let e=[eY,q.configure({forceFocusDelay:200}),L];return Z&&e.push(Q.Eq),e},[Z,L]),W=(0,u.useMemo)(()=>[P,F],[P,F]),V=d.isTeamAiSummaryEnabled(D),K=d.isAiSummaryEnabled,{updateUserPreferences:er}=function(){let e=(0,g.MU)();return{updateUserPreferences:async t=>{await e.send({eventName:"UpdateUserPreferences",dest:{component:s.wA.Main},data:{preferences:t}})}}}();(function(e){let t=(0,g.MU)(),{teamId:n,globallySyncedStore:r,foldersStore:i}=e;(0,u.useEffect)(()=>{async function e(){await v(t,i,n),r.lastSelected?.folderId&&i.selectFolderById(r.lastSelected.folderId)}i.isLoading||e()},[e.teamId])})({globallySyncedStore:d,authStore:l,foldersStore:i,teamId:D}),function(e){let t=(0,g.MU)(),{userId:n,inAppNotificationsStore:r}=e;(0,u.useEffect)(()=>{async function e(){if(!n)return;r.setLoading(!0);let e=await t.send({eventName:"GetInAppNotifications",data:null,dest:{component:s.wA.Main,location:void 0}}).finally(()=>r.setLoading(!1));r.update(e)}r.loading||e()},[n,t,r])}({userId:E,inAppNotificationsStore:n});let ei=(0,g.EO)(),{hasReachedLimit:ea}=k(),eo=V&&K&&!ea,[es,el]=function(e){let[t,n]=(0,u.useState)(null),r=e.getIntegration(t??"");return(0,u.useEffect)(()=>{if(t&&r)return(0,f.U5)(()=>r.userConfigured,t=>{t&&(e.selectIntegration(r),n(null))})},[t,e,r]),[t,n]}(t),ed=ei.screenshot.screenshotIsCaptured&&null===ei.screenshot.compositeScreenshot,ec=t.isLoadingIntegrationFields||"pre_draft"===c.state.name||"submission"===c.state.name||ed,eu=c.type===eI.K8.Video&&("pre_draft"===c.state.name||"draft"===c.state.name)?c.state.payload.toolsSummary:null,[ep,eg]=(0,u.useState)(null),[em,ex]=(0,u.useState)(!1),eh=e=>{if(o.setContentSnapshot(e),Z){let n=(e.content?.[0]?.content??[]).map(e=>e.text??"").join("");t.setFieldValue("title",n)}},ef=function(e){let t=(0,u.useRef)(null);t.current||(t.current=function(){let e=new Map;return{dismiss:t=>{let n=ni(t),r=e.get(n);r&&e.set(n,{...r,dismissed:!0})},get:t=>{if(!t.enabled)return{state:nn};let n=ni(t.params),r=e.get(n);if(r)return{promise:r.promise,state:na(r)};let i=(0,A.Z)(),a=nr(t.broker,t.params,i).then(t=>{let r=e.get(n),i=r?.dismissed?{...t,dismissed:!0}:t;return e.set(n,i),na(i)}).catch(()=>{let t=e.get(n),r={...nn,dismissed:t?.dismissed??!1,sessionId:i,status:"error"};return e.set(n,r),na(r)}),o={...nn,promise:a,sessionId:i,status:"loading"};return e.set(n,o),{promise:a,state:na(o)}},getAcceptedIds:t=>{let n=ni(t),r=e.get(n);return r?.sessionId&&r?.generationId?{sessionId:r.sessionId,generationId:r.generationId}:null}}}());let n=(0,g.rC)(),{editor:r,query:i}=e,{hasTitle:a,onAcceptedContent:o}=r,{params:l}=i;return{onCreate:e=>{let r=t.current?.get(i);r&&(r.state.sessionId&&n.setSessionId(r.state.sessionId),no(e,r.state,a),r.promise?.then(t=>{t.sessionId&&n.setSessionId(t.sessionId),e.isDestroyed||no(e,t,a)}),e.on("transaction",({transaction:n})=>{n.getMeta("acceptSuggestion")&&(o(e.getJSON()),t.current?.dismiss(l),function(e,t,n){let r=n?.getAcceptedIds(t);r&&e.send({eventName:"NotifyAiGenerationAccepted",dest:{component:s.wA.Main,location:void 0},data:{aiSessionId:r.sessionId,aiGenerationId:r.generationId}})}(i.broker,l,t.current))}))},onUnmount:e=>{let n=null!==ns(e);((0,Y.tZ)(e)||n)&&t.current?.dismiss(l),n&&o(e.getJSON())}}}({editor:{hasTitle:Z,onAcceptedContent:eh},query:{broker:b,enabled:eo&&c.type===eI.K8.Video,params:{tabId:w,teamId:D,draftStartedAt:c.type===eI.K8.Video&&"draft"===c.state.name?c.state.payload.startTimestamp:void 0}}}),ev=d.user?.teams.find(e=>e.id===D),eb=ev?.roleType===eI.GD.ViewerRestricted,ew=(d.user?.teams??[]).some(e=>e.roleType!==eI.GD.ViewerRestricted);if((0,u.useEffect)(()=>{if(!eb||ew)return;let e=b.send({eventName:"NewToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:w},data:{title:"No permission to create Jams in this workspace",icon:"warning",dismissable:!0}});return()=>{e.then(e=>b.send({eventName:"RemoveToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:w},data:{toastId:e?.toastId}}))}},[eb,ew,b,w]),!ev)return null;let ey=d.myFeatures,eC=eu?function(e,t){let n=[];switch((e?.blur.numBlurredSelectors??-1)>0&&!t.hasAccess(S.AN.CaptureScreenRecordingBlur,"any")&&0>=t.numDemoUsesRemaining(S.AN.CaptureScreenRecordingBlur)&&n.push("blur"),e?.annotations.didUseAnnotations&&!t.hasAccess(S.AN.CaptureScreenRecordingAnnotations,"any")&&0>=t.numDemoUsesRemaining(S.AN.CaptureScreenRecordingAnnotations)&&n.push("annotations"),n.length){case 0:return;case 1:return`Please upgrade to use the ${n[0]} feature`;case 2:return`Please upgrade to use the ${n.join(" and ")} features`;default:return"Please upgrade to use these features"}}(eu,ey):void 0,ej="draft"===c.state.name&&c.state.payload.resumedDraft,eS=eb||ea?"Save to drafts":"Create",e$=t.getFileTypes(),eN=o.attachments.filter(e=>nl(e$,e.type)).map(e=>({id:e.id,name:e.name,type:e.type,src:e.source}));return(0,r.jsx)(nu,{"data-testid":"comment-modal",children:(0,r.jsxs)(np,{ref:eg,children:[(0,r.jsxs)(ng,{children:[(0,r.jsx)(eF,{closeJam:e.closeJam,resumedDraft:ej}),e.children]}),(0,r.jsx)(nm,{children:(0,r.jsxs)(nx,{children:[(0,r.jsx)(et.v,{integrations:t}),(0,r.jsx)(ne,{authStore:e.authStore,myFeaturesStore:ey,integrationsStore:t,waitingForAuth:es,setWaitingForAuth:el}),(0,r.jsx)(nh,{children:(0,r.jsx)(X.H4,{ref:x,content:(0,Q.DE)(o.getMessageContent(),Z),onChange:eh,onCreate:ef.onCreate,onUnmount:ef.onUnmount,onSubmit:e.handleCreateThread,extensions:U,suggestions:W,suggestionSide:"bottom"},`${String(Z)}:${String(eo)}`)}),(0,r.jsx)(N.k,{px:"3",children:(0,r.jsx)(O,{attachments:eN,onRemove:o.removeAttachment})}),(0,r.jsx)(en.V,{tooltipContainer:ep,integrations:t}),(0,r.jsx)(nf,{children:(0,r.jsx)(nc,{teamId:D,onUpgrade:e=>ek(D,e,{[$.t1.SOURCE]:"extension:iframe",[$.t1.CONTENT]:"draft-modal-banner"}),toolsSummary:eu,myFeatures:ey,shouldShowAiGenerationBanner:eo,teamFeatureUsage:p})}),(0,r.jsx)("input",{ref:h,type:"file",multiple:!0,hidden:!0,onChange:e=>{let t=Array.from(e.target.files??[]);t.length>0&&C(t),e.target.value=""}}),(0,r.jsxs)(N.k,{minWidth:"0",p:"4",children:[(0,r.jsxs)(N.k,{flexGrow:"1",minWidth:"0",align:"center",gap:"2",pr:"3",children:[e$?.type!==eI.Wz.None&&(0,r.jsx)(R.u,{content:"Attach files",children:(0,r.jsx)(z.h,{size:"1",variant:"ghost",color:"gray",onClick:()=>h.current?.click(),children:(0,r.jsx)(ee,{size:16})})}),(0,r.jsx)(e7,{foldersStore:i}),V&&c.type===eI.K8.Video&&(0,r.jsx)(eQ,{enabled:K&&!ea,locked:ea,lockedReason:"You've reached your Jam quota. AI is locked until your quota resets.",onChange:e=>er({aiSummaryEnabled:e})})]}),(0,r.jsx)(R.u,{content:eC??"",hidden:!eC,children:(0,r.jsx)(M.z,{loading:em,onClick:async()=>{if(eb||ea){e.closeJam({showToast:!0,storeDraft:!0});return}ex(!0);try{await e.handleCreateThread()}finally{ex(!1)}},disabled:em||ec||(eb?ej:!!eC),children:eS})})]})]})})]})})}),nc=(0,c.Pi)(e=>{let{onUpgrade:t,toolsSummary:n,myFeatures:i,shouldShowAiGenerationBanner:a,teamId:o}=e,s=e.teamFeatureUsage.get(o,S.AN.TeamJamQuotaLimit);if(s&&s.limit>-1){if(!(s.remaining<=5))return;let e=s.remaining<=0,n=`You have ${s.remaining}`,i=e?(0,r.jsxs)(r.Fragment,{children:["You've reached your monthly limit.",(0,r.jsx)("br",{})," New Jams are saved as drafts."]}):`${n} ${eA()("Jam",s.limit)} left this month.`;return(0,r.jsx)(eo,{text:i,feature:S.AN.TeamJamQuotaLimit,onUpgrade:t,limitReached:e})}return(n?.blur.numBlurredSelectors??-1)>0&&!i.hasAccess(S.AN.CaptureScreenRecordingBlur,"any")&&0>=i.numDemoUsesRemaining(S.AN.CaptureScreenRecordingBlur)?(d.k.warn("Showing special-case `0 demo uses remaining` banner",{featureName:"blur"}),(0,r.jsx)(eh,{feature:S.AN.CaptureScreenRecordingBlur,store:i,onUpgrade:t,text:(e,t)=>`${e}/${t} ${eA()("video blur",t)} left`})):n?.annotations.didUseAnnotations&&!i.hasAccess(S.AN.CaptureScreenRecordingAnnotations,"any")&&0>=i.numDemoUsesRemaining(S.AN.CaptureScreenRecordingAnnotations)?(d.k.warn("Showing special-case `0 demo uses remaining` banner",{featureName:"annotations"}),(0,r.jsx)(eh,{feature:S.AN.CaptureScreenRecordingAnnotations,store:i,onUpgrade:t,text:(e,t)=>`${e}/${t} ${eA()("video annotation",t)} left`})):a?(0,r.jsx)(eh,{dismissable:!0,feature:S.AN.AiSummaryGeneration,store:i,onUpgrade:t,text:(e,t)=>`${e}/${t} ${eA()("AI summary",t)} left`}):null}),nu=i.Z.div`
  padding: 24px;
  max-width: 100%;
  max-height: 100%;
  min-height: 340px;

  width: 90%;
  height: 90%;
  ${ey.w.mobile} {
    padding: 0;
  }
`,np=i.Z.div`
  display: flex;
  width: 100%;
  height: 100%;

  ${ey.w.tablet} {
    flex-direction: column;
  }

  box-shadow: 0px 4px 32px rgba(0, 0, 0, 0.2);
  border-radius: 16px;
`,ng=i.Z.div`
  padding: ${eg.W.SP600};
  display: flex;
  flex-direction: column;
  background: ${eC.O.lightGrey};
  border-top-left-radius: 16px;
  border-bottom-left-radius: 16px;
  position: relative;
  z-index: 1;
  min-width: 0; // fix flex overflow
  flex: 1;
  justify-content: center;
  ${ey.w.tablet} {
    border-radius: 16px 16px 0 0;
  }
`,nm=i.Z.div`
  display: flex;
  position: relative;
  background: ${eC.O.white};
  width: 372px;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;

  ${ey.w.tablet} {
    width: auto;
    border-radius: 0 0 16px 16px;
    overflow: auto;
  }
`,nx=i.Z.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;

  ${ey.w.tablet} {
    height: max-content;
  }
`,nh=i.Z.div`
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
`,nf=i.Z.div`
  padding: 0 16px;

  &:empty {
    display: none;
  }
`;async function nv(e){let{broker:t,integrationsStore:n,globallySyncedStore:r}=e,i=r.currentTab.id,o=function(e){if(e.hasSelectedIntegration()){let t=e.invalidFieldValues,n=e.selectedIntegration?.displayName;if(t)return{title:`Some ${n} values are invalid.`,description:t.map(e=>e.message).join(", "),icon:"warning",ttl:a.eq("3s")};if(e.displayFieldsLoading)return{title:`${n} fields are currently loading, please wait.`,icon:"warning",ttl:a.eq("2s")}}}(n);if(o){(0,m.G)(t,i,o);return}n.storeRecentlyUsedFields();let s=n.hasSelectedIntegration()?n.onSubmitUserMessage:"Creating a link for you, on its way shortly!",{toastId:l}=await (0,m.G)(t,i,{title:s,ttl:a.eq("2m"),icon:"loading"});return{toastId:l}}let nb=(0,c.Pi)(function(e){let[t,n]=(0,u.useState)("idle"),i=(0,g.dR)(),c=(0,g.$7)(),f=(0,g.b3)(),v=(0,g.Pn)(),w=(0,g.fe)(),S=(0,g.__)(),k=(0,g.MU)(),I=function(e=x){let[t,n]=(0,u.useState)(void 0),r=(0,g.MU)(),[i,a]=(0,u.useState)(0),[o,l]=(0,u.useState)(),d=(0,g.dR)().currentTab.id,c=(0,m.i)();async function p(){l((await c({title:"Press esc again to close Jam",icon:"info"})).toastId)}return(0,u.useEffect)(()=>()=>{o&&r.send({eventName:"RemoveToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:d},data:{toastId:o}}),window.clearTimeout(t)},[t,o,r,d]),async function(){if(void 0===o&&await p(),Date.now()-i<e.gracePeriodMs){await r.send({eventName:"RemoveToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:d},data:{toastId:o}}),l(void 0),await r.send({eventName:"Dismiss",dest:{component:s.wA.Main,location:void 0},data:{}});return}a(Date.now()),n(window.setTimeout(()=>{r.send({eventName:"RemoveToast",dest:{component:s.wA.ContentScript,location:s.Ye.ContentScripts.JamUi,tabId:d},data:{toastId:o}}),l(void 0)},e.gracePeriodMs))}}(),$=j();!function(e){let[t,n]=(0,u.useState)(!1),r=(0,g.MU)(),i=(0,g.rC)(),a=(0,g.b3)(),o=(0,g.__)(),l=(0,g.Pn)(),c=(0,g.$7)().selectedTeamId;(0,u.useEffect)(()=>{(async function(){if("draft"===e.state.name&&e.state.payload?.resumedDraft&&!t)try{d.k.info(`resuming ${e.type} draft`);let t=await r.send({eventName:"GetDraftResumableState",dest:{component:s.wA.Main,location:void 0},data:null});if(t.ok){let{message:n,aiSessionState:s,folderId:u,integrationState:p,attachments:g}=t.value;d.k.info(`resuming ${e.type} draft with data`,{message:!!n,aiSessionState:!!s,folderId:!!u,integrationState:!!p,attachments:!!g}),s?.sessionId&&b(()=>i.resumeSessionState(s),"restoring aiSessionState",{aiSessionState:s}),n&&b(()=>a.setInitialContentFromJSON(n),"restoring message",{message:n}),g&&b(()=>a.addAttachments(g),"restoring attachments",{teamId:c,attachmentCount:g?.length}),await Promise.all([C(r,o,c,u).catch(e=>{d.k.error("error on restoring folder",{error:(0,h.LT)(e),folderId:u,teamId:c})}),y(l,p,c).catch(e=>{d.k.error("error on restoring integration state",{error:(0,h.LT)(e),teamId:c,integrationName:p?.integrationName})})])}d.k.info(`resumed ${e.type} draft successfully`)}catch(e){d.k.error("failed to or resume part of the draft state",{error:(0,h.LT)(e),teamId:c})}finally{n(!0)}})()},[e,t,c,r,i,a,o,l])}(i.capture),(0,u.useEffect)(()=>()=>{k.send({eventName:"FreezeClickEvents",dest:{component:s.wA.HostScript,location:s.Ye.HostScripts.AdditionalHooks,tabId:i.currentTab.id},data:!1})},[k,i.currentTab.id]);let A=(0,u.useRef)(null);return"complete"===t?null:(0,r.jsx)(nw,{ref:A,submitState:t,children:(0,r.jsx)(o.V,{fullScreen:!0,open:!0,onClose:I,disablePortal:!0,borderRadius:32,backgroundColor:"transparent",children:(0,r.jsx)(nd,{globallySyncedStore:i,newThreadStore:f,integrationsStore:v,inAppNotificationsStore:w,foldersStore:S,authStore:c,handleCreateThread:async()=>{try{let e=await (0,l.Y)().create("jam_create",{createTimeout:a.eq("1s"),traceTimeout:a.eq("1m")});d.k.debug("jam_create trace result",{traceResult:e})}catch(e){d.k.error("jam_create trace error",{error:e})}try{$()}catch(e){d.k.warn("jam_create syncContextUp error",{error:e})}let t=await nv({broker:k,integrationsStore:v,globallySyncedStore:i});t&&(e.onBeforeSubmit&&((0,p.flushSync)(()=>{n("in-progress")}),await e.onBeforeSubmit()),await e.onSubmit(t),n("complete"))},closeJam:async(e={})=>{await k.send({eventName:"Dismiss",dest:{component:s.wA.Main,location:void 0},data:e})},children:e.children})})})}),nw=i.Z.div`
  position: relative;
  pointer-events: auto;
  padding: 32px;

  opacity: ${e=>"in-progress"===e.submitState||"complete"===e.submitState?0:1};
  transition: opacity 0.1s;
`},16140:function(e,t,n){n.d(t,{Z:()=>a});var r=n(63403),i=n(49710);async function a(e){let t=e.captureType===i.K8.Screenshot?"CreateJamScreenshot":e.captureType===i.K8.Video?"CreateJamVideo":"CreateJamReplay";return e.broker.send({eventName:t,dest:{component:r.wA.Main,location:void 0},data:e.data})}}};
//# sourceMappingURL=558.js.map