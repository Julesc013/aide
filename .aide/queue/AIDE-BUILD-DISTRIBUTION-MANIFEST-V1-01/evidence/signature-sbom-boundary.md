# Signature And SBOM Boundary

This build supports signature and SBOM references/placeholders only.

It does not claim:

- verified signatures;
- generated SBOM;
- SLSA/in-toto attestation;
- release trust;
- public publication.

False verified-signature claims fail with:

```text
distribution.signature_unverified
```

Generated-SBOM claims fail with:

```text
distribution.sbom_unavailable
```
