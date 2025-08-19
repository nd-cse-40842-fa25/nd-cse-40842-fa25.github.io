# Configuration

DOCROOT=	public
WWWROOT=	weasel:$(HOME)/www/courses/cse.40842.fa25
YASB=		scripts/yasb.py

# Rules

build:
	@$(YASB)

install:	build
	@rsync -av --progress --delete \
		--include='courses/*.html' \
		--exclude='archive' \
		--exclude='courses/*' \
		$(DOCROOT)/. $(WWWROOT)/.

clean:
	@echo Cleaning...
	@rm -fr $(DOCROOT)
