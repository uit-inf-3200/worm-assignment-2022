.PHONY: default

default: worm-assignment.pdf ../README.md \
    ../README.html\
    ../worm_gate/README.html\
    ../python_zip_example/README.html\

PDF_OPTS := --citeproc

# For the GitHub-flavored README.md from the more featureful Pandoc Markdown

# Standalone is necessary to render the table of contents
README_OPTS := --standalone --toc --citeproc
# Shift headings one size smaller to all fit under the main h1 for the page
README_OPTS += --shift-heading-level-by=1
# Output as GitHub-flavored Markdown, minus the YAML metadata block
# (which GitHub now shows as a big ugly table at the top of the page)
README_OPTS += --to gfm-yaml_metadata_block

worm-assignment.pdf: worm-assignment.md $(wildcard *.bib) $(wildcard *.csl)
	pandoc $(PDF_OPTS) $< -o $@

../README.md: worm-assignment.md $(wildcard *.bib) $(wildcard *.csl)
	pandoc $(README_OPTS) $< -o $@

# For the READMEs, create a preview HTML to check the rendering
%.html: %.md
	pandoc --standalone --from gfm $< -o $@
