import json
from exceptions import FioOutputParseError


def parse_fio_output(results):
    """
    Парсит результаты выполнения fio тестов и извлекает латентность для
    операций randread и randwrite.
    """
    data = {"randread": [], "randwrite": []}
    for iodepth, output in results:
        try:
            fio_data = json.loads(output)
            print(fio_data)
            jobs = fio_data["jobs"][0]
            if "read" in jobs:
                latency = jobs["read"]["lat_ns"]["mean"] / 1e6
                data["randread"].append((iodepth, latency))
            if "write" in jobs:
                latency = jobs["write"]["lat_ns"]["mean"] / 1e6
                data["randwrite"].append((iodepth, latency))
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            error_message = (
                f"Error while parsing fio output for iodepth={iodepth}. "
                f"Exception: {str(e)}"
            )
            raise FioOutputParseError(error_message) from e
    return data
