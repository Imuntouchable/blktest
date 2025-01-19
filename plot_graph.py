import tempfile
import os
import subprocess
from exceptions import GnuplotError, GnuplotScriptError


def generate_gnuplot_script(data, output_file):
    """Генерация скрипта для gnuplot для построения графика."""
    if "randread" not in data or "randwrite" not in data:
        raise GnuplotScriptError(
            "Data must contain both 'randread' and 'randwrite' keys."
        )
    gnuplot_script = f"""
    set terminal png size 800,600
    set output "{output_file}"
    set title "Latency vs IODEPTH"
    set xlabel "IODEPTH"
    set ylabel "Latency (ms)"
    set grid
    plot '-' using 1:2 with linespoints title "Randread", \\
        '-' using 1:2 with linespoints title "Randwrite"
    """
    try:
        for iodepth, latency in data["randread"]:
            gnuplot_script += f"{iodepth} {latency}\n"
    except TypeError:
        raise GnuplotScriptError(
            "Expected data in 'randread' to be a list of tuples."
        )
    gnuplot_script += "e\n"
    try:
        for iodepth, latency in data["randwrite"]:
            gnuplot_script += f"{iodepth} {latency}\n"
    except TypeError:
        raise GnuplotScriptError(
            "Expected data in 'randwrite' to be a list of tuples."
        )
    gnuplot_script += "e\n"
    return gnuplot_script


def run_gnuplot(script):
    """Запуск gnuplot с генерируемым скриптом."""
    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            mode='w'
        ) as temp_script:
            temp_script.write(script)
            temp_script_path = temp_script.name
        subprocess.run(["gnuplot", temp_script_path], check=True)
    except subprocess.CalledProcessError as e:
        raise GnuplotError(f"Error running gnuplot: {e}")
    except Exception as e:
        raise GnuplotError(f"Unexpected error: {e}")
    finally:
        if os.path.exists(temp_script_path):
            os.unlink(temp_script_path)
