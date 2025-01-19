import argparse
import logging
from fio_test import run_fio_test
from parse_fio import parse_fio_output
from plot_graph import generate_gnuplot_script, run_gnuplot
from exceptions import FioParseError, FioTestError


logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Test block device performance with fio and plot results."
    )
    parser.add_argument(
        "--name", required=True, help="Test name"
    )
    parser.add_argument(
        "--filename", required=True, help="Path to the file for testing"
    )
    parser.add_argument(
        "--output", required=True, help="Path to save the output graph"
    )
    args = parser.parse_args()

    try:
        logger.info(
            f"Starting fio test for randread with name: {args.name}, "
            f"filename: {args.filename}"
        )
        fio_results_read = run_fio_test(
            args.name,
            args.filename,
            args.output,
            "randread"
        )
        if not fio_results_read:
            raise FioTestError("fio tests for randread failed.")

        logger.info(
            f"Starting fio test for randwrite with name: {args.name}, "
            f"filename: {args.filename}"
        )
        fio_results_write = run_fio_test(
            args.name,
            args.filename,
            args.output,
            "randwrite"
        )
        if not fio_results_write:
            raise FioTestError("fio tests for randwrite failed.")
        data_read_write = {
            "randread": parse_fio_output(fio_results_read)["randread"],
            "randwrite": parse_fio_output(fio_results_write)["randwrite"]
        }
        gnuplot_script = generate_gnuplot_script(data_read_write, args.output)
        run_gnuplot(gnuplot_script)
        logger.info(f"Graph saved to {args.output}")

    except FioTestError as e:
        logger.error(f"Test error: {e}")
    except FioParseError as e:
        logger.error(f"Parsing error: {e}")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
