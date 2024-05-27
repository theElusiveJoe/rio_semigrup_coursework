create_venv:
	python3 -m venv venv
	chmod +x ./venv/bin/activate
	./venv/bin/activate
	./venv/bin/python3 -m pip install -r requirements.txt

test_all:
	cd src
	./venv/bin/activate
	pytest --verbose .

_setup:
	cd src
	./venv/bin/activate

demo_graph_processor:
	make _setup
	python3 src/cmd/demo_graph_processor.py

	
demo_isom_builder_graph:
	make _setup
	python3 src/cmd/demo_isom_builder_draw_graph.py

	
demo_isom_builder:
	make _setup
	python3 src/cmd/demo_isom_builder.py

	
demo_military:
	make _setup
	python3 src/cmd/demo_military.py

	