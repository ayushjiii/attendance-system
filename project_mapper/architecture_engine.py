from pathlib import Path
import json
import networkx as nx


class ArchitectureEngine:

    
    # INITIALIZATION
    

    def __init__(self):

        self.snapshot_file = Path(
            "snapshots/snapshot.json"
        )

        self.snapshot = {}

        self.apps = []

        self.models = {}

        self.dependencies = {}

        self.graph = nx.DiGraph()

        self.load_snapshot()

        self.build_graph()


    
    # LOAD SNAPSHOT
    

    def load_snapshot(self):

        with open(
            self.snapshot_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.snapshot = json.load(f)


        self.apps = self.snapshot.get(
            "apps",
            []
        )

        self.models = self.snapshot.get(
            "models",
            {}
        )

        self.dependencies = self.snapshot.get(
            "dependencies",
            {}
        )


    
    # BUILD GRAPH


    def build_graph(self):

        for source, targets in self.dependencies.items():

            for target in targets:

                self.graph.add_edge(
                    source,
                    target
                )


    
    # CENTRAL APPS
    

    def get_central_apps(self):

        scores = {}


        for source, targets in self.dependencies.items():

            scores[source] = (
                scores.get(source, 0)
                + len(targets)
            )


            for target in targets:

                scores[target] = (
                    scores.get(target, 0)
                    + 1
                )


        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )


        return ranked


    
    # IMPACT ANALYSIS
    

    def analyze_impact(self, node):

        try:

            return nx.descendants(
                self.graph,
                node
            )

        except nx.NetworkXError:

            return set()


    
    # WORKFLOW ANALYSIS
    

    def find_workflow(self, keyword):

        keyword = keyword.lower()

        workflows = []


        for app in self.graph.nodes:

            if keyword in app.lower():

                descendants = nx.descendants(
                    self.graph,
                    app
                )


                workflow = [app]

                workflow.extend(
                    sorted(descendants)
                )


                workflows.append(workflow)


        return workflows