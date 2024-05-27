# Run

!!! set env PYTHONPATH variable before and setup virtual environment run
```
export PYTHONPATH="$(pwd)/src"
make create_venv
```

run scripts

the best way is to use **makefile**

manually:
```
cd src
python3 cmd/<script_name>.py
```

* `demo_military` --- demonstration of military algorithm work
* `demo_graph_processor` --- demonstration of H-classes search
* `demo_isom_builder` --- demonstration of isomorphism builder algorithm
* `demo_isom_builder_draw_graph` --- demonstration of isomorphism builder algorithm with graph building

Results of `demo_isom_builder_draw_graph` and `demo_military` are sored in `outpur` folder.


# References

### Military algo

Original paper: https://www.irif.fr/~jep/PDF/Rio.pdf
Original code: https://www.irif.fr/~jep/Logiciels/Semigroupe2.0/semigroupe2.html

Check Initialisation.c and Calcul.c files.
