# naming agent — prompt
A plugin needs a name. Published slugs are IMMUTABLE (LOOP.md: names are forever),
so choose at spec stage like it's permanent. Generate candidates, then run
tools/naming.py check on each — exclude exact collisions, near-collisions (same
letters/different separators), reserved words, and malformed slugs. Propose the
clean candidates to the owner's desk with one-tap selection, recorded before any
install command spreads.
