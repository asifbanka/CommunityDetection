target = main

all: main.pdf 

theplots:
	../benchmark/makeallplots.sh json plots

bib:
	pdflatex $(target).tex
	-bibtex --min-crossrefs=99 $(target) # Ignore bibtex errors
	-bibtex --min-crossrefs=99 short
	pdflatex $(target).tex
	@pdflatex $(target).tex

.PHONY: bib clean again

again: 
	touch main.tex
	make main.pdf
	
%.pdf: %.tex
	pdflatex $<
	@pdflatex $< # for references

main.pdf: header.tex the_model.tex major_algorithms.tex intro.tex setup.tex non_overlapping.tex plots.tex overlapping.tex

%.pdf: %.ps
	ps2pdf $< 2> /dev/null # Warnings are bad for vim

%.dvi: %.tex
	latex $< 
	@latex $< # Again for references

clean:
	rm -f *.aux *.bbl *.log *.dvi 2> /dev/null
