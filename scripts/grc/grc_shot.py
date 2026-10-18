"""Run a compiled GRC qt_gui flowgraph headless, optionally set variables, and save a screenshot.
usage: grc_shot.py module.py out.png seconds [var=value ...]"""
import sys, importlib.util, signal
from PyQt5 import Qt
spec = importlib.util.spec_from_file_location("fg", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cls = [v for k, v in vars(m).items() if isinstance(v, type) and issubclass(v, Qt.QWidget) and hasattr(v, 'start')][0]
app = Qt.QApplication(sys.argv[:1])
tb = cls()
for kv in sys.argv[4:]:
    k, v = kv.split('=')
    win = getattr(tb, '_' + k + '_win', None)
    boxes = win.findChildren(Qt.QDoubleSpinBox) if win is not None else []
    if boxes:
        boxes[0].setValue(float(v))      # move the GUI control, which calls set_<k>
    else:
        getattr(tb, 'set_' + k)(float(v))
tb.resize(1060, 560); tb.start(); tb.show()
def done():
    tb.grab().save(sys.argv[2]); tb.stop(); tb.wait(); app.quit()
Qt.QTimer.singleShot(int(float(sys.argv[3]) * 1000), done)
app.exec_()
print("saved", sys.argv[2])
