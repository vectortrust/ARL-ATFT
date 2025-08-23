LATEX=pdflatex
BIB=biber
MAIN=main

.PHONY: all clean

all:
	$(LATEX) $(MAIN).tex || true
	$(BIB) $(MAIN) || true
	$(LATEX) $(MAIN).tex || true
	$(LATEX) $(MAIN).tex || true

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.lof *.lot
	rm -f $(MAIN).pdf

