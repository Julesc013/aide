# Legacy Candidate Prioritization

## Criteria

- documented extensibility or integration surface
- ecosystem coverage value beyond Microsoft, Apple, and CodeWarrior
- likely feasibility of obtaining runnable environments
- clarity of source material
- value for cross-era architectural learning

## Near-term candidates

- `eclipse.platform`
  - Strong documented plug-in model, broad ecosystem reach, and high architectural reuse value.
- `apache.netbeans`
  - Strong module system, active project, and clear cross-platform relevance.
- `oracle.developer-studio`
  - Valuable Unix and Solaris coverage with an official IDE surface, though likely harder than Eclipse or NetBeans.

## Valuable but difficult

- `embarcadero.rad-studio-lineage`
  - High Windows value and documented Tools API, but proprietary tooling and environment reconstruction cost are likely higher.
- `kde.kdevelop`
  - Good Linux coverage, but this prompt did not collect enough API detail to rank it with Eclipse or NetBeans yet.
- `openwatcom.ide`
  - Good archival coverage across DOS, OS/2, and Windows, but environment and tooling reconstruction will likely dominate the work.

## Archival or research-first

- `ibm.visualage-cpp-os2`
  - Historically important, but environment acquisition and documentation fidelity are weaker than the near-term set.

## Why CodeWarrior is already committed

- CodeWarrior already had a committed host-family scaffold in the repository before this prompt.
- The preserved source set for CodeWarrior includes a documented native SDK and automation surface, which is stronger than many other archival IDE families.
- The legacy candidate families above remain candidates because they still need lane decisions, environment evidence, and deeper host-contract normalization before promotion into `hosts/`.
