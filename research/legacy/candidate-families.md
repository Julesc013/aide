# Legacy Candidate Families

This atlas is curated. It is not exhaustive.

## Older Windows

### `embarcadero.rad-studio-lineage`

- Display name: Embarcadero RAD Studio / Delphi / C++Builder lineage
- Vendor or project: Embarcadero
- Why it matters: long-lived native IDE line on Windows with a documented Tools API and clear historical continuity from Borland and CodeGear tooling.
- Likely support mode bias: `native`
- Likely adapter strategy: native IDE package or add-in contract
- Source quality: official current docs for the modern line; earlier Borland-era continuity is partly inferential.
- Sources:
  - https://docwiki.embarcadero.com/RADStudio/Sydney/en/Extending_the_IDE_Using_the_Tools_API
  - https://www.embarcadero.com/products/cbuilder

## OS/2

### `ibm.visualage-cpp-os2`

- Display name: IBM VisualAge C++ for OS/2 lineage
- Vendor or project: IBM
- Why it matters: represents a historically important OS/2-native IDE family and a distinct IBM tooling ecosystem.
- Likely support mode bias: `archival`
- Likely adapter strategy: companion-first, with native work only if acceptable documentation and runnable environments can be reconstructed later.
- Source quality: mixed official and archived official, but weaker than the modern cross-platform families.
- Sources:
  - https://www.ibm.com/support/pages/ibm-cc-compilers-os2-version-365-fix-pack-2-us-english
  - https://public.dhe.ibm.com/ps/products/db2/info/vr6/htm/db2ax/db2ax63.htm

## Unix and workstation

### `oracle.developer-studio`

- Display name: Oracle Developer Studio / Sun Studio / WorkShop lineage
- Vendor or project: Oracle
- Why it matters: covers Solaris and Unix-workstation history with a documented IDE component and long-lived compiler/debugger stack.
- Likely support mode bias: `native`
- Likely adapter strategy: native IDE integration if the NetBeans-based layer proves reachable; companion fallback otherwise.
- Source quality: strong official and archived official coverage.
- Sources:
  - https://www.oracle.com/application-development/technologies/developerstudio.html
  - https://docs.oracle.com/cd/E60778_01/html/E60744/gkofj.html
  - https://docs.oracle.com/cd/E19059-01/stud.9/817-6691/817-6691.pdf

## Cross-platform and Linux-heavy

### `eclipse.platform`

- Display name: Eclipse Platform IDE lineage
- Vendor or project: Eclipse Foundation
- Why it matters: broad ecosystem coverage, well-documented plug-in model, and high reuse potential for future cross-host adapter work.
- Likely support mode bias: `native`
- Likely adapter strategy: documented plug-in lane using PDE and related runtime contracts.
- Source quality: foundation-official and strong.
- Sources:
  - https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/guide/intro/pde_overview.htm
  - https://www.eclipse.org/articles/Whitepaper-Platform-3.1/eclipse-platform-whitepaper.pdf

### `apache.netbeans`

- Display name: Apache NetBeans
- Vendor or project: Apache NetBeans
- Why it matters: cross-platform IDE family with a documented module system and current plug-in distribution path.
- Likely support mode bias: `native`
- Likely adapter strategy: module-based native integration.
- Source quality: project-official and strong.
- Sources:
  - https://netbeans.apache.org/front/main/about
  - https://netbeans.apache.org/tutorials/nbm-dukescript.html
  - https://plugins.netbeans.apache.org/

### `kde.kdevelop`

- Display name: KDevelop
- Vendor or project: KDE
- Why it matters: strong Linux and Unix-era relevance with continued current distribution.
- Likely support mode bias: `native`
- Likely adapter strategy: native plug-in or component integration, pending deeper API research.
- Source quality: project-official but thinner on extensibility details in this prompt.
- Sources:
  - https://kdevelop.org/
  - https://apps.kde.org/kdevelop/

## DOS, OS/2, and archival toolchains

### `openwatcom.ide`

- Display name: Open Watcom IDE lineage
- Vendor or project: Open Watcom Project
- Why it matters: covers DOS, OS/2, and Windows-era tooling with preserved graphical-tool documentation and strong archival value.
- Likely support mode bias: `legacy-native`
- Likely adapter strategy: archival native or companion-first, depending how much of the graphical tooling is reconstructable in practice.
- Source quality: project-official and suitable for candidate tracking.
- Sources:
  - https://openwatcom.org/
  - https://openwatcom.org/ftp/manuals/current/guitool.pdf

## Fact, inference, unresolved

- Fact: every candidate listed above has at least one official, archived official, foundation-official, or project-official source in this prompt's source log.
- Inference: the likely support modes and likely adapter strategies are architectural judgments, not commitments.
- Unresolved: earlier DOS Turbo lineages and several niche workstation IDEs remain outside this initial curated set because the current prompt favored documentation quality and adapter relevance over raw breadth.
