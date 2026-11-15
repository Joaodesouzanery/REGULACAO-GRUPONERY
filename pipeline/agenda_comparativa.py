"""Atalho: python3 pipeline/agenda_comparativa.py clientes/<x>/<pasta>  (= pipeline/monitoramento.py <pasta> agenda)"""
import sys, os, subprocess
sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitoramento.py"), sys.argv[1], "agenda"]))
