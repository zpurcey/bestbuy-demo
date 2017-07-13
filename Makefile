
.PHONY=help
help::
	@echo "Install virtualenv and dependencies first (see README)"
	@echo ""
	@echo "Then run:"
	@echo "make backend #Run backend service on http://localhost:5000"
	@echo "make frontend #Run frontend service on http://localhost:8000"
	@echo
	@echo "After performing the above, point your browser to http://localhost:8000"

.PHONY=frontend
frontend::
	#(cd frontend && python -m http.server)
	(cd frontend && python -m  SimpleHTTPServer)

.PHONY=backend
backend::
	python runbackend.py
