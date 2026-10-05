# Research-question hypothesis schematics

Generator for the inert SVG illustrations registered against question guides in
`analysis/research/registry.json`. It lives under `docs/` because it is
documentation tooling: it produces explanatory figures, never a scientific
result, and no value it draws comes from data.

[make_rq_schematics_v1.py](make_rq_schematics_v1.py) emits the A28, A29 and A30
illustrations into each question's `RQ_Specified/<dir>/schematics/` folder.

## Why the output is hand-built SVG

The research gate accepts a registered illustration only if it is an SVG using
`svg`, `title`, `desc`, `rect`, `line`, `ellipse`, `polygon`, `text` and `a`,
with no `style` attributes, no event handlers, no `url()` references and any
link pinned to a repository blob. Exports from general-purpose figure tools
carry `path`, `g`, `defs` and inline styles and are rejected, so these are
drawn from primitives.

## Layout

Each plate is the experiment a reader would set up, not a diagram of the
argument: the arms as culture dishes or sample strata, the readouts measured on
every arm, then an outcome-to-conclusion table. Rival explanations appear as
alternative rows of that table, which is where a bench scientist meets them.

Re-running the generator changes the file bytes, so the registered
`schematic_sha256` in the registry must be refreshed in the same commit.
