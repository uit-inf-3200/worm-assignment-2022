.PHONY: default

default: worm-assignment.pdf ../README.md \
    ../README.html\
    ../worm_gate/README.html\
    ../python_zip_example/README.html\

PDF_OPTS := --citeproc

# Note that --standalone is necessary to render the toc and the header-includes.
# However, --standalone also preserves the YAML block at the top, and GitHub
# now renders that block in an ugly horizontal table at the top of the README.
# To avoid the ugly table, turn off the 'yaml_metadata_block' extension in the
# output format.
README_OPTS := --standalone --toc --citeproc
README_OPTS += --shift-heading-level-by=1 --to gfm-yaml_metadata_block

worm-assignment.pdf: worm-assignment.md $(wildcard *.bib) $(wildcard *.csl)
	pandoc $(PDF_OPTS) $< -o $@

../README.md: worm-assignment.md $(wildcard *.bib) $(wildcard *.csl)
	pandoc $(README_OPTS) $< -o $@

%.html: %.md
	pandoc --from gfm $< -o $@
