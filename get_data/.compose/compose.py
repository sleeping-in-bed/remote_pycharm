from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from get_dynamic_compose import get_dc

get_dc().fd_all().up()
