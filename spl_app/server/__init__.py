"""
Server module for SPL gRPC application.
"""
from .spl_server import SPLRepositoryServicer, serve

__all__ = ['SPLRepositoryServicer', 'serve']
