"""Load a .grc with GRC's own platform and save it back, filling every default."""
import sys
from gnuradio import gr
from gnuradio.grc.core.platform import Platform
p = Platform(name='GNU Radio Companion Compiler', prefs=gr.prefs(), version=gr.version(),
             version_parts=(gr.major_version(), gr.api_version(), gr.minor_version()))
p.build_library()
for path in sys.argv[1:]:
    fg = p.make_flow_graph(path)
    fg.rewrite(); fg.validate()
    errs = fg.get_error_messages()
    if errs:
        print(path, 'ERRORS:', errs); sys.exit(1)
    p.save_flow_graph(path, fg)
    print('normalized', path)
