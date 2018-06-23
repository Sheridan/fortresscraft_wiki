from pygraphviz import *
import re
from gamedata_parser.model.fceitem import FCEItem
from gamedata_parser.model.fceresearch import FCEResearch
from gamedata_parser.jsonbase import JsonBase

debug = True

class GraphsCompiler(JsonBase):
    def __init__(self, media_dir):
        super(GraphsCompiler, self).__init__(media_dir)
        self._graphviz_dir = '%s/graphviz' % (self._media_dir)
        self._digraph = {'nodes': {}, 'edges': []}
        self._site = 'https://fortresscraft.info' if debug else ''

    def _add_node(self, name, label):
        self._digraph['nodes'][name] = {'label': label}

    def _add_research_node(self, name, node_data):
        project_item_requirements = []
        if 'project_item_requirements' in node_data:
            for project_item_requirement in node_data['project_item_requirements'].keys():
                with FCEItem(self._media_dir, project_item_requirement) as item:
                    project_item_requirements.append('<tr><td target="{site}/index.php?title=FCEItem::{name}"><img src="icons/32/{name}.png" /></td><td>{item_name}</td><td>{amount}</td></tr>'.format(
                        site=self._site,
                        name=item.name,
                        item_name=item.data['name'],
                        amount=node_data['project_item_requirements'][project_item_requirement]
                    ))
        items=''
        if len(project_item_requirements):
            items='<table>%s</table>' % (''.join(project_item_requirements))
        self._digraph['nodes'][name] = {
            'shape': 'plaintext',
            'label': '''<<table>
            <tr><td colspan="2">{caption}</td></tr>
            <tr>
                <td target="{site}/index.php?title=FCEResearch::{name}"><img src="icons/64/{name}.png" /></td>
                <td>{items}</td>
            </tr>
            </table>>'''.format(
                caption=node_data['name'],
                site=self._site,
                name=name,
                items=items
            )
            }

    def _add_edge(self, src_name, dst_name):
        self._digraph['edges'].append({'src': src_name, 'dst': dst_name})

    def _compile_research_tree(self):
        for processing_file in self._get_json_list('research'):
            processing_data = self._load_json(processing_file)
            self._add_research_node(processing_data['index_name'], processing_data)
            if 'research_requirement' in processing_data:
                for research_requirement in processing_data['research_requirement']:
                    self._add_edge(research_requirement, processing_data['index_name'])

    def _render(self):
        # print(self._digraph)
        with open('%s/dot/research.dot' % (self._graphviz_dir), 'w') as f:
            f.write('digraph G {')
            for node_name in self._digraph['nodes'].keys():
                node_data = self._digraph['nodes'][node_name]
                # print(node_data)
                node_options = []
                for key in node_data.keys():
                    node_options.append('%s=%s' % (key, node_data[key]))
                f.write('%s [%s];\n' % (
                    node_name,
                    ','.join(node_options)
                    ))
            for edge_data in self._digraph['edges']:
                f.write('{0} -> {1};\n'.format(
                    edge_data['src'],
                    edge_data['dst']
                    ))
            f.write('}')



    def compile(self):
        self._compile_research_tree()
        self._render()

