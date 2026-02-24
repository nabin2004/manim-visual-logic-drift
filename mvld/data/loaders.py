import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

class TikZLoader:
    """
    Parses TikZ LaTeX code to extract spatial information.
    Focuses on \draw commands and basic shapes.
    """
    def __init__(self):
        # Basic patterns for TikZ parsing
        self.draw_pattern = re.compile(r'\\draw\s*(?:\[.*?\])?\s*(.*?);', re.DOTALL)
        self.coord_pattern = re.compile(r'\(([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\)')
        self.shape_pattern = re.compile(r'(circle|rectangle|ellipse|node)')

    def parse_string(self, content: str) -> List[Dict[str, Any]]:
        results = []
        draws = self.draw_pattern.findall(content)
        
        for draw in draws:
            coords = self.coord_pattern.findall(draw)
            shape_match = self.shape_pattern.search(draw)
            
            if coords:
                # Convert string coords to floats
                points = [[float(c[0]), float(c[1])] for c in coords]
                
                entry = {
                    "type": shape_match.group(0) if shape_match else "path",
                    "points": points,
                    "raw": draw.strip()
                }
                
                # Approximate center for shapes
                if entry["type"] in ["circle", "rectangle", "ellipse"] and len(points) >= 1:
                    entry["center"] = points[0]
                elif entry["type"] == "path" and len(points) >= 2:
                    # avg of start/end
                    entry["center"] = [(points[0][0] + points[-1][0])/2, (points[0][1] + points[-1][1])/2]
                    
                results.append(entry)
        
        return results

class SVGLoader:
    """
    Parses SVG files to extract basic spatial primitives.
    """
    def parse_file(self, file_path: Path) -> List[Dict[str, Any]]:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Remove namespace for easier querying
        for el in root.iter():
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
        
        return self._parse_element(root)

    def parse_string(self, content: str) -> List[Dict[str, Any]]:
        root = ET.fromstring(content)
        for el in root.iter():
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
        return self._parse_element(root)

    def _parse_element(self, element: ET.Element) -> List[Dict[str, Any]]:
        results = []
        
        for child in element:
            tag = child.tag
            data = {"type": tag, "raw_attrs": dict(child.attrib)}
            
            if tag == "circle":
                data.update({
                    "center": [float(child.get("cx", 0)), float(child.get("cy", 0))],
                    "radius": float(child.get("r", 0))
                })
                results.append(data)
            elif tag == "rect":
                w, h = float(child.get("width", 0)), float(child.get("height", 0))
                x, y = float(child.get("x", 0)), float(child.get("y", 0))
                data.update({
                    "center": [x + w/2, y + h/2],
                    "width": w,
                    "height": h
                })
                results.append(data)
            elif tag == "path":
                # Path parsing is complex; for pretraining we might just take 
                # a bounding box or starting point.
                data["d"] = child.get("d")
                results.append(data)
                
            # Recursive for groups <g>
            if tag == "g":
                results.extend(self._parse_element(child))
                
        return results

if __name__ == "__main__":
    # Quick test
    tikz_data = r"\draw (0,0) circle (1); \draw[blue] (2,2) rectangle (4,4);"
    loader = TikZLoader()
    print("TikZ Results:", loader.parse_string(tikz_data))
    
    svg_data = '<svg><circle cx="50" cy="50" r="40"/><rect x="10" y="10" width="30" height="30"/></svg>'
    svg_loader = SVGLoader()
    print("SVG Results:", svg_loader.parse_string(svg_data))
