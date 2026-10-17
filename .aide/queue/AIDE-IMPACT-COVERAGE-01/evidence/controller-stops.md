# Controller preparation stops

Before source staging, git plan reported dirty_tree_requires_classification for the
exact31 reviewed source paths. No effect occurred; exact classification was retained
and only the reviewed source commit proceeded. A later input-pin preflight initially
iterated a mapping as records and stopped with TypeError before manifest/job launch.
Corrected controller iteration to path/hash pairs, preserving every pin and effect.
Neither stop allocated a job or changes the original source-test failure.
