
import os

from mlblocks import discovery

from datatracer.core import PRETRAINED_DIR, DataTracer
from datatracer.data import get_demo_data, load_dataset, load_datasets

_BASE_PATH = os.path.abspath(os.path.dirname(__file__))
_JSONS_PATH = os.path.join(_BASE_PATH, 'jsons')
MLBLOCKS_PRIMITIVES = os.path.join(_JSONS_PATH, 'primitives')
MLBLOCKS_PIPELINES = os.path.join(_JSONS_PATH, 'pipelines')


__all__ = (
    'DataTracer',
    'get_demo_data',
    'get_pipelines',
    'get_primitives',
    'load_dataset',
    'load_datasets',
)


def get_pipelines():

    return discovery.find_pipelines('datatracer')


def get_primitives():

    return discovery.find_primitives('datatracer')


def get_solvers():

    return [
        pretrained_solver[:-3]
        for pretrained_solver in os.listdir(PRETRAINED_DIR)
        if pretrained_solver.endswith('.dt')
    ]
