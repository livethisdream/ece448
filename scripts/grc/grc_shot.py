"""Run a compiled GRC qt_gui flowgraph headless, optionally set variables, and save a screenshot.
usage: grc_shot.py [--size WxH] module.py out.png seconds [var=value ...]

--size sets the window (default 1060x560); a flowgraph with more than one row
of plots needs a taller one. An Audio Sink opens ALSA's null device, so a
flowgraph that plays audio runs in a container with no sound card."""
import os, sys, tempfile, importlib.util
args = sys.argv[1:]
W, H = 1060, 560
if args and args[0] == '--size':
    W, H = map(int, args[1].lower().split('x')); args = args[2:]
if 'ALSA_CONFIG_PATH' not in os.environ:
    conf = tempfile.NamedTemporaryFile('w', suffix='.conf', delete=False)
    conf.write('pcm.!default { type null }\nctl.!default { type hw card 0 }\n'); conf.close()
    os.environ['ALSA_CONFIG_PATH'] = conf.name
module, out, seconds, settings = args[0], args[1], float(args[2]), args[3:]
sys.path.insert(0, os.path.dirname(os.path.abspath(module)))   # embedded Python blocks sit beside the module
from PyQt5 import Qt
spec = importlib.util.spec_from_file_location("fg", module); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cls = [v for k, v in vars(m).items() if isinstance(v, type) and issubclass(v, Qt.QWidget) and hasattr(v, 'start')][0]
app = Qt.QApplication(sys.argv[:1])
tb = cls()
for kv in settings:
    k, v = kv.split('=')
    win = getattr(tb, '_' + k + '_win', None)
    boxes = win.findChildren(Qt.QDoubleSpinBox) if win is not None else []
    if boxes:
        boxes[0].setValue(float(v))      # move the GUI control, which calls set_<k>
    else:
        getattr(tb, 'set_' + k)(float(v))
tb.resize(W, H); tb.start(); tb.show()
def done():
    tb.grab().save(out); tb.stop(); tb.wait(); app.quit()
Qt.QTimer.singleShot(int(seconds * 1000), done)
app.exec_()
print("saved", out)
