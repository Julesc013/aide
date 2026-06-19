# Warning Disposition

The result is `ACCEPTED_WITH_WARNINGS`.

Warnings are accepted because the missing capabilities are explicitly deferred
and the accepted slice fails closed:

- no adapter admission;
- no trust;
- no adapter execution;
- no sandbox creation;
- no credential resolution;
- no provider/model/Gateway/network calls;
- no GitHub mutation;
- no patch apply or target mutation;
- no runtime, Service, Commander, Workbench, Test Broker, or ContextPack v2;
- no full JSON Schema Draft validation.
