"""
CFG Branch Analyzer - Specialized for analyzing branch information in control flow graphs to improve branch coverage
"""
import networkx as nx
from typing import Dict, List, Tuple, Set, Optional
from .cfg.src.comex.codeviews.CFG.CFG_driver import CFGDriver
from .cfg.src.comex.codeviews.combined_graph.combined_driver import line_number_to_node_id_mapping
from .utils import read_file
from .panta_logger import pantaLogger


class CFGBranchAnalyzer:
    """
    CFG Branch Analyzer - Specialized for extracting and analyzing branch information 
    from control flow graphs to improve unit test branch coverage
    """
    
    def __init__(self, language: str, source_code: str):
        self.language = language
        self.source_code = source_code
        self.logger = pantaLogger.initialize_logger(__name__)
        
        # Initialize CFG driver
        self.cfg_driver = CFGDriver(language, source_code)
        self.graph = self.cfg_driver.graph
        self.cfg_nodes = self.cfg_driver.CFG_nodes
        self.cfg_node_map = self.cfg_driver.CFG_node_map
        self.cfg_edge_map = self.cfg_driver.CFG_edge_map
        
        # Get line number mapping
        _, self.node_id_to_line_number = line_number_to_node_id_mapping(
            source_code, self.cfg_nodes
        )
        
        # Analyze branch information
        self.branch_info = self._analyze_branches()
        self.conditional_branches = self._extract_conditional_branches()
        self.loop_branches = self._extract_loop_branches()
        self.exception_branches = self._extract_exception_branches()
    
    def _analyze_branches(self) -> Dict:
        """
        Analyze all branch information in the CFG
        """
        branch_info = {
            'conditional_branches': [],
            'loop_branches': [],
            'exception_branches': [],
            'switch_branches': [],
            'branch_coverage_hints': []
        }
        
        for edge in self.graph.edges():
            source_node, target_node = edge
            edge_label = self.cfg_edge_map.get((source_node, target_node))
            
            if edge_label in ['pos_next', 'neg_next']:
                # Conditional branches
                branch_info['conditional_branches'].append({
                    'source': source_node,
                    'target': target_node,
                    'condition': self.cfg_node_map.get(source_node, ('', ''))[0],
                    'edge_label': edge_label,
                    'lines': self.node_id_to_line_number.get(source_node, []),
                    'branch_type': 'true' if edge_label == 'pos_next' else 'false'
                })
            elif edge_label == 'catch_exception':
                # Exception branches
                branch_info['exception_branches'].append({
                    'source': source_node,
                    'target': target_node,
                    'condition': self.cfg_node_map.get(source_node, ('', ''))[0],
                    'lines': self.node_id_to_line_number.get(source_node, []),
                    'branch_type': 'exception'
                })
        
        return branch_info
    
    def _extract_conditional_branches(self) -> List[Dict]:
        """
        Extract conditional branch information
        """
        conditional_branches = []
        
        for edge in self.graph.edges():
            source_node, target_node = edge
            edge_label = self.cfg_edge_map.get((source_node, target_node))
            
            if edge_label in ['pos_next', 'neg_next']:
                source_statement = self.cfg_node_map.get(source_node, ('', ''))[0]
                source_lines = self.node_id_to_line_number.get(source_node, [])
                
                conditional_branches.append({
                    'node_id': source_node,
                    'statement': source_statement,
                    'lines': source_lines,
                    'true_branch': target_node if edge_label == 'pos_next' else None,
                    'false_branch': target_node if edge_label == 'neg_next' else None,
                    'edge_label': edge_label,
                    'complexity': self._calculate_branch_complexity(source_node)
                })
        
        return conditional_branches
    
    def _extract_loop_branches(self) -> List[Dict]:
        """
        Extract loop branch information
        """
        loop_branches = []
        
        for node_id in self.cfg_nodes:
            node_type = self.cfg_node_map.get(node_id, ('', ''))[1]
            if node_type in ['for_statement', 'while_statement', 'do_statement']:
                loop_branches.append({
                    'node_id': node_id,
                    'statement': self.cfg_node_map.get(node_id, ('', ''))[0],
                    'lines': self.node_id_to_line_number.get(node_id, []),
                    'loop_type': node_type,
                    'successors': list(self.graph.successors(node_id))
                })
        
        return loop_branches
    
    def _extract_exception_branches(self) -> List[Dict]:
        """
        Extract exception handling branch information
        """
        exception_branches = []
        
        for edge in self.graph.edges():
            source_node, target_node = edge
            edge_label = self.cfg_edge_map.get((source_node, target_node))
            
            if edge_label == 'catch_exception':
                exception_branches.append({
                    'source': source_node,
                    'target': target_node,
                    'statement': self.cfg_node_map.get(source_node, ('', ''))[0],
                    'lines': self.node_id_to_line_number.get(source_node, []),
                    'exception_type': 'catch'
                })
        
        return exception_branches
    
    def _calculate_branch_complexity(self, node_id: int) -> int:
        """
        Calculate branch complexity
        """
        complexity = 0
        for edge in self.graph.edges():
            if edge[0] == node_id:
                edge_label = self.cfg_edge_map.get(edge)
                if edge_label in ['pos_next', 'neg_next']:
                    complexity += 1
        return complexity
    
    def get_branch_coverage_hints(self, missed_branches: List[int]) -> List[Dict]:
        """
        Generate test hints based on uncovered branches
        """
        hints = []
        
        for branch_line in missed_branches:
            # Find branch nodes containing this line
            for branch in self.conditional_branches:
                if branch_line in branch['lines']:
                    hint = {
                        'branch_line': branch_line,
                        'statement': branch['statement'],
                        'suggested_test_conditions': self._generate_test_conditions(branch),
                        'branch_type': branch['edge_label'],
                        'complexity': branch['complexity']
                    }
                    hints.append(hint)
                    break
        
        return hints
    
    def _generate_test_conditions(self, branch: Dict) -> List[str]:
        """
        Generate test condition suggestions for branches
        """
        conditions = []
        statement = branch['statement']
        
        if 'if' in statement.lower():
            # Extract condition expression
            if '(' in statement and ')' in statement:
                condition = statement[statement.find('(')+1:statement.find(')')]
                conditions.append(f"Test case where condition '{condition}' evaluates to True")
                conditions.append(f"Test case where condition '{condition}' evaluates to False")
        
        elif 'while' in statement.lower() or 'for' in statement.lower():
            conditions.append(f"Test case that enters the loop")
            conditions.append(f"Test case that skips the loop")
        
        return conditions
    
    def get_method_branch_analysis(self, method_name: str) -> Dict:
        """
        Get branch analysis for a specific method
        """
        method_branches = []
        
        # Find method corresponding nodes
        for node_id in self.cfg_nodes:
            node_statement = self.cfg_node_map.get(node_id, ('', ''))[0]
            if method_name in node_statement and 'method_declaration' in self.cfg_node_map.get(node_id, ('', ''))[1]:
                # Analyze all branches within this method
                method_branches = self._analyze_method_branches(node_id)
                break
        
        return {
            'method_name': method_name,
            'branches': method_branches,
            'total_branches': len(method_branches),
            'conditional_branches': len([b for b in method_branches if b['type'] == 'conditional']),
            'loop_branches': len([b for b in method_branches if b['type'] == 'loop']),
            'exception_branches': len([b for b in method_branches if b['type'] == 'exception'])
        }
    
    def _analyze_method_branches(self, method_start_node: int) -> List[Dict]:
        """
        Analyze branches within a specific method
        """
        method_branches = []
        
        # Get all nodes in the method
        method_nodes = self._get_method_nodes(method_start_node)
        
        for node_id in method_nodes:
            node_type = self.cfg_node_map.get(node_id, ('', ''))[1]
            node_statement = self.cfg_node_map.get(node_id, ('', ''))[0]
            
            if node_type in ['if_statement', 'while_statement', 'for_statement', 'switch_statement']:
                # Analyze branches for this node
                branches = self._get_node_branches(node_id)
                for branch in branches:
                    branch['method_node'] = node_id
                    branch['method_statement'] = node_statement
                    method_branches.append(branch)
        
        return method_branches
    
    def _get_method_nodes(self, start_node: int) -> List[int]:
        """
        Get all nodes within a method
        """
        # This needs to be implemented according to the actual CFG structure
        # Simplified implementation, returns all reachable nodes from start_node
        visited = set()
        queue = [start_node]
        method_nodes = []
        
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                method_nodes.append(node)
                for successor in self.graph.successors(node):
                    if successor not in visited:
                        queue.append(successor)
        
        return method_nodes
    
    def _get_node_branches(self, node_id: int) -> List[Dict]:
        """
        Get branch information for a specific node
        """
        branches = []
        
        for edge in self.graph.edges():
            if edge[0] == node_id:
                edge_label = self.cfg_edge_map.get(edge)
                target_node = edge[1]
                
                branch_info = {
                    'source': node_id,
                    'target': target_node,
                    'edge_label': edge_label,
                    'lines': self.node_id_to_line_number.get(node_id, []),
                    'type': self._get_branch_type(edge_label)
                }
                branches.append(branch_info)
        
        return branches
    
    def _get_branch_type(self, edge_label: str) -> str:
        """
        Determine branch type based on edge label
        """
        if edge_label in ['pos_next', 'neg_next']:
            return 'conditional'
        elif edge_label == 'catch_exception':
            return 'exception'
        elif 'loop' in edge_label:
            return 'loop'
        else:
            return 'other'
    
    def generate_branch_coverage_prompt(self, missed_branches: List[int]) -> str:
        """
        Generate prompt text for branch coverage
        """
        hints = self.get_branch_coverage_hints(missed_branches)
        
        if not hints:
            return ""
        
        prompt = "\n=== Branch Coverage Guidance ===\n"
        prompt += "The following branches need special attention to improve branch coverage:\n\n"
        
        for i, hint in enumerate(hints, 1):
            prompt += f"{i}. Line {hint['branch_line']}: {hint['statement']}\n"
            prompt += f"   Branch type: {hint['branch_type']}\n"
            prompt += f"   Complexity: {hint['complexity']}\n"
            prompt += "   Suggested test conditions:\n"
            for condition in hint['suggested_test_conditions']:
                prompt += f"   - {condition}\n"
            prompt += "\n"
        
        return prompt
