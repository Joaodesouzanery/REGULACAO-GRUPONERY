"""Atalho: python3 pipeline/raio_x.py clientes/<x>/<pasta>  (= pipeline/monitoramento.py <pasta> raio_x)"""
import sys, os, subprocess
sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitoramento.py"), sys.argv[1], "raio_x"]))
