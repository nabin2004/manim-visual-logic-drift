from mvld.data.loaders import TikZLoader, SVGLoader
import json

def test_loaders():
    tikz_content = r"""
    \begin{tikzpicture}
    \draw (0,0) circle (1cm);
    \draw (2,3) rectangle (4,5);
    \draw (1,1) -- (2,2);
    \end{tikzpicture}
    """
    
    svg_content = """
    <svg width="100" height="100">
      <circle cx="20" cy="20" r="10" fill="red" />
      <rect x="50" y="50" width="20" height="20" fill="blue" />
    </svg>
    """
    
    tikz_loader = TikZLoader()
    svg_loader = SVGLoader()
    
    print("--- TikZ Parsing ---")
    tikz_res = tikZ_loader.parse_string(tikz_content)
    print(json.dumps(tikz_res, indent=2))
    
    print("\n--- SVG Parsing ---")
    svg_res = svg_loader.parse_string(svg_content)
    print(json.dumps(svg_res, indent=2))

if __name__ == "__main__":
    test_loaders()
