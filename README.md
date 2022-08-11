# Horus

## Code Example

### Plot a networkx graph with matplotlib

```console
poetry run python -m src.horus.pipelines.matplotlib_vis_networkx_pipeline -png tests/data/example_graph.json -pvng tests/data/output/example_graph.png
```

### Plot a networkx with pygraphviz

```console
poetry run python -m src.horus.pipelines.pygraphviz_networkx_pipeline -png data/01_raw/len_2_sequence_labelled_intermediate_graph.json -pvng data/02_intermediate/pygraphviz_networkx.png --edge-label
```
