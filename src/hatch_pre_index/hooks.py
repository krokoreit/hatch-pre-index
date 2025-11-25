from hatchling.plugin import hookimpl
from hatch_pre_index import PreIndexPublisher

@hookimpl
def hatch_register_publisher():
    return PreIndexPublisher
