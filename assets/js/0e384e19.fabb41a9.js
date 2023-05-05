"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[9671],{3905:(t,e,o)=>{o.d(e,{Zo:()=>p,kt:()=>b});var n=o(7294);function r(t,e,o){return e in t?Object.defineProperty(t,e,{value:o,enumerable:!0,configurable:!0,writable:!0}):t[e]=o,t}function i(t,e){var o=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),o.push.apply(o,n)}return o}function a(t){for(var e=1;e<arguments.length;e++){var o=null!=arguments[e]?arguments[e]:{};e%2?i(Object(o),!0).forEach((function(e){r(t,e,o[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(o)):i(Object(o)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(o,e))}))}return t}function s(t,e){if(null==t)return{};var o,n,r=function(t,e){if(null==t)return{};var o,n,r={},i=Object.keys(t);for(n=0;n<i.length;n++)o=i[n],e.indexOf(o)>=0||(r[o]=t[o]);return r}(t,e);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(t);for(n=0;n<i.length;n++)o=i[n],e.indexOf(o)>=0||Object.prototype.propertyIsEnumerable.call(t,o)&&(r[o]=t[o])}return r}var c=n.createContext({}),l=function(t){var e=n.useContext(c),o=e;return t&&(o="function"==typeof t?t(e):a(a({},e),t)),o},p=function(t){var e=l(t.components);return n.createElement(c.Provider,{value:e},t.children)},d="mdxType",u={inlineCode:"code",wrapper:function(t){var e=t.children;return n.createElement(n.Fragment,{},e)}},m=n.forwardRef((function(t,e){var o=t.components,r=t.mdxType,i=t.originalType,c=t.parentName,p=s(t,["components","mdxType","originalType","parentName"]),d=l(o),m=r,b=d["".concat(c,".").concat(m)]||d[m]||u[m]||i;return o?n.createElement(b,a(a({ref:e},p),{},{components:o})):n.createElement(b,a({ref:e},p))}));function b(t,e){var o=arguments,r=e&&e.mdxType;if("string"==typeof t||r){var i=o.length,a=new Array(i);a[0]=m;var s={};for(var c in e)hasOwnProperty.call(e,c)&&(s[c]=e[c]);s.originalType=t,s[d]="string"==typeof t?t:r,a[1]=s;for(var l=2;l<i;l++)a[l]=o[l];return n.createElement.apply(null,a)}return n.createElement.apply(null,o)}m.displayName="MDXCreateElement"},9881:(t,e,o)=>{o.r(e),o.d(e,{assets:()=>c,contentTitle:()=>a,default:()=>u,frontMatter:()=>i,metadata:()=>s,toc:()=>l});var n=o(7462),r=(o(7294),o(3905));const i={sidebar_position:1},a="Introduction",s={unversionedId:"intro",id:"intro",title:"Introduction",description:"Application to manage and track a stocks portfolio with dividends and return for a Buy & Hold investment investment strategy.",source:"@site/docs/intro.md",sourceDirName:".",slug:"/intro",permalink:"/buho-stocks/docs/intro",draft:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/intro.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",next:{title:"Introduction",permalink:"/buho-stocks/docs/deploy-application/introduction"}},c={},l=[{value:"Motivation",id:"motivation",level:2},{value:"Development",id:"development",level:2},{value:"Deployment",id:"deployment",level:2},{value:"User guides",id:"user-guides",level:2}],p={toc:l},d="wrapper";function u(t){let{components:e,...o}=t;return(0,r.kt)(d,(0,n.Z)({},p,o,{components:e,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"introduction"},"Introduction"),(0,r.kt)("p",{align:"center"},(0,r.kt)("img",{src:"/buho-stocks/img/logo.png",alt:"Buho-Stocks logo",style:{width:200}})),(0,r.kt)("p",{align:"center"},"Application to manage and track a stocks portfolio with dividends and return for a ",(0,r.kt)("a",{href:"https://en.wikipedia.org/wiki/Buy_and_hold",title:"Wikipedia"},"Buy & Hold investment")," investment strategy."),(0,r.kt)("p",{align:"center"},(0,r.kt)("img",{src:"https://github.com/bocabitlabs/buho-stocks/actions/workflows/django.yml/badge.svg",href:"https://github.com/bocabitlabs/buho-stocks/actions/workflows/django.yml",alt:"Django CI"})," ",(0,r.kt)("img",{src:"https://github.com/bocabitlabs/buho-stocks/actions/workflows/react.yml/badge.svg",href:"https://github.com/bocabitlabs/buho-stocks/actions/workflows/react.yml",alt:"React CI"})," ",(0,r.kt)("a",{href:"https://codecov.io/gh/bocabitlabs/buho-stocks",title:"CodeCov"},(0,r.kt)("img",{src:"https://codecov.io/gh/bocabitlabs/buho-stocks/branch/main/graph/badge.svg",alt:"codecov"}))),(0,r.kt)("h2",{id:"motivation"},"Motivation"),(0,r.kt)("p",null,"Using a spreadsheet to manage a portfolio can become a complicated and tedious task, as well as calculating investment returns. That's why I decided to create this application, to simplify these periodic and monotonous tasks of portfolio management."),(0,r.kt)("h2",{id:"development"},"Development"),(0,r.kt)("p",null,"If you are a developer and want to contribute, please check the ",(0,r.kt)("a",{parentName:"p",href:"https://github.com/bocabitlabs/buho-stocks/blob/main/.github/CONTRIBUTING.md"},"Contribution guideliness")," and the ",(0,r.kt)("a",{parentName:"p",href:"/docs/development/requirements"},"Development guides")),(0,r.kt)("h2",{id:"deployment"},"Deployment"),(0,r.kt)("p",null,"Do you want to deploy the application in production? The documentation to it is available on ",(0,r.kt)("a",{parentName:"p",href:"/docs/deploy-application/introduction"},"Deploy application")),(0,r.kt)("h2",{id:"user-guides"},"User guides"),(0,r.kt)("p",null,"User guides will be added to this section when available."))}u.isMDXComponent=!0}}]);