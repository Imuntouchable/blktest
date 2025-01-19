import subprocess
import logging
from exceptions import FioTestError

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_fio_test(name, filename, output, rw_mode):
    """Запуск теста fio с указанными параметрами."""
    iodepth_values = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    results = []

    for iodepth in iodepth_values:
        fio_command = [
            "fio",
            f"--name={name}",
            f"--filename={filename}",
            "--ioengine=libaio",
            "--direct=1",
            "--bs=4K",
            "--size=1G",
            "--numjobs=1",
            f"--rw={rw_mode}",
            f"--iodepth={iodepth}",
            "--output-format=json",
            "--thread"
        ]

        try:
            logger.info(
                f"Running fio test with iodepth={iodepth} "
                f"and rw_mode={rw_mode}..."
            )
            result = subprocess.run(
                fio_command,
                capture_output=True,
                text=True,
                check=True
            )
            results.append((iodepth, result.stdout))
        except subprocess.CalledProcessError as e:
            error_message = (
                f"fio test failed for iodepth={iodepth} "
                f"and rw_mode={rw_mode}. Error: {e.stderr}"
            )
            logger.error(error_message)
            raise FioTestError(error_message) from e
        except Exception as e:
            error_message = (
                f"Unexpected error during fio test with iodepth={iodepth} "
                f"and rw_mode={rw_mode}."
            )
            logger.error(error_message)
            raise FioTestError(error_message) from e

    return results
